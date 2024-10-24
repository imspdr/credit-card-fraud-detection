import logging
import threading
import numpy as np
import hpbandster.core.nameserver as hpns
from hpbandster.optimizers import BOHB
from hpbandster.core.worker import Worker
from numpy.ma.extras import average

from .config_parser import ConfigParser
from .model_runner import ModelRunner
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, recall_score, confusion_matrix, accuracy_score, precision_score

'''
Traner using BOHB optimization module

Recorder : record result from each worker and track best config & loss
Worker : run train and evaluating for each iteration of bayesian optimization
Trainer : run bohb optimization and deal informations
'''

class Recorder:
    def __init__(self):
        self.lock = threading.Lock()
        self.best_loss = np.inf
        self.best_config = None

    def update(self, loss, config):
        self.lock.acquire()
        logging.info("loss : %s" % str(loss))
        logging.info("config : %s" % str(config))
        if self.best_loss > loss:
            self.best_loss = loss
            self.best_config = config
        self.lock.release()



class MyWorker(Worker):
    def __init__(self, division, config_parser, recorder, col_names, **kwargs):
        super().__init__(**kwargs)
        self.config_parser = config_parser
        self.division = division
        self.col_names = col_names
        self.recorder = recorder

    def compute(self, config, budget, **kwargs):
        # load model runner with given config
        try:
            pp = ModelRunner(**self.config_parser.bohb_config2model_runner(config))
            k = len(self.division)
        except ValueError:
            status = "model loading error"
            logging.error(status)
            return {
                "loss": -1,
                "info": {"config": config, "budget": budget},
            }

        # k-fold cross validation
        score = []
        for i in range(k):
            now_X_test = self.division[i][0]
            now_y_test = self.division[i][1]
            now_X_train_list = []
            now_y_train_list = []
            for j in range(k):
                if j != i:
                    now_X_train_list.append(self.division[j][0])
                    now_y_train_list.append(self.division[j][1])
            now_X_train = np.vstack(now_X_train_list)
            now_y_train = np.hstack(now_y_train_list)
            pp.train(now_X_train, now_y_train, self.col_names)
            y_hat = pp.inference(now_X_test)
            f1 = f1_score(now_y_test, y_hat, average="weighted")
            score.append(1 - f1)
        mean_loss = np.mean(score)

        self.recorder.update(mean_loss, config)
        return {
            "loss": mean_loss,
            "info": {"config": config, "budget": budget},
        }


class Trainer:
    def __init__(self, custom_model=None):
        if custom_model:
            self.config_parser = ConfigParser(custom_model=custom_model)
        else:
            self.config_parser = ConfigParser()
        self.recorder = Recorder()
        self.best_model = None
        self.best_loss = {}

    def train_with_hpo(self, X, y, col_names, n_worker=1, n_iter=20):
        '''
        :param X: input (numpy ndarray)
        :param y: output (numpy ndarray)
        :param col_names: (list of string)
        :param n_worker: (int)
        :param n_iter: (int)
        :return: void
        '''

        '''
        STEP 1. data division
        '''
        # divide data to 6
        # one for hold out and use 5 partition for 5-fold cross validation
        k = 6
        logging.info("[trainer] start data division")
        division = []
        for i in range(k - 1):
            X_rest, X_part, y_rest, y_part = train_test_split(X, y, test_size=1 / (k - i),  stratify=y)
            division.append([X_part, y_part])
            X = X_rest
            y = y_rest
        division.append([X, y])

        '''
        STEP 2. Bayesian optimization
        '''
        logging.info("[trainer] start name server")
        self.recorder = Recorder()
        name_server = hpns.NameServer(run_id="trainer", host="127.0.0.1", port=None)
        name_server.start()
        for i in range(n_worker):
            worker = MyWorker(
                division[:-1],
                col_names=col_names,
                config_parser=self.config_parser,
                recorder=self.recorder,
                run_id="trainer",
                nameserver="127.0.0.1",
                id=i,
            )
            worker.run(background=True)

        logging.info("[trainer] generate configspace")
        configspace = self.config_parser.build_bohb_config()

        logging.info("[trainer] start bohb")

        # set both budget 1.0 to use only bayesian optimization
        bohb = BOHB(
            configspace=configspace,
            run_id="trainer",
            nameserver="127.0.0.1",
            min_budget=1.0,
            max_budget=1.0,
        )
        bohb.run(n_iterations=n_iter)
        bohb.shutdown(shutdown_workers=True)
        name_server.shutdown()

        logging.info("[trainer] train end")
        logging.info("[trainer] evaluate model with hold-out set")

        '''
        STEP 3. Evaluate best model
        '''
        # load best model
        temp_best_model = ModelRunner(
            **self.config_parser.bohb_config2model_runner(self.recorder.best_config)
        )

        # train with full data (5 division) and evaluate it for hold out
        X_train_list = []
        y_train_list = []
        for i in range(k - 1):
            X_train_list.append(division[i][0])
            y_train_list.append(division[i][1])
        X_train = np.vstack(X_train_list)
        y_train = np.hstack(y_train_list)
        X_test, y_test = division[-1]
        temp_best_model.train(X_train, y_train, col_names)
        y_hat = temp_best_model.inference(X_test)
        f1 = f1_score(y_test, y_hat, average="weighted")
        recall = recall_score(y_test, y_hat, average="weighted")
        accuracy = accuracy_score(y_test, y_hat)
        precision = precision_score(y_test, y_hat, average="weighted")

        self.best_loss = {
            "f1": f1,
            "recall": recall,
            "precision": precision,
            "accuracy": accuracy
        }
        '''
        STEP 4. save & train with full data
        '''
        # train with full data and save model
        logging.info("[trainer] save best model")
        self.best_model = ModelRunner(**self.config_parser.bohb_config2model_runner(self.recorder.best_config))
        self.best_model.train(X, y, col_names)
        return self.best_model

    def report(self):
        return {
            "best_config": self.best_model.get_config(),
            "best_loss": self.best_loss,
            "feature_importance": self.best_model.get_model().feature_importance(),
        }
