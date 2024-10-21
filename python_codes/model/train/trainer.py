import logging
import threading
import numpy as np
import hpbandster.core.nameserver as hpns
from hpbandster.optimizers import BOHB
from hpbandster.core.worker import Worker
from .config_parser import ConfigParser
from .model_runner import ModelRunner
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix


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

def evaluate_loss(y_test, y_hat):
    f1 = f1_score(y_test, y_hat, average="weighted")
    acc = accuracy_score(y_test, y_hat)
    return f1, acc, (f1 + acc) / 2

def my_confusion_matrix(y_test, y_hat):
    uniques = np.unique(y_hat)
    class_value = confusion_matrix(y_test, y_hat, labels=uniques)
    return class_value, uniques


class MyWorker(Worker):
    def __init__(self, division, config_parser, recorder, col_names, **kwargs):
        super().__init__(**kwargs)
        self.config_parser = config_parser
        self.division = division
        self.col_names = col_names
        self.recorder = recorder

    def compute(self, config, budget, **kwargs):
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
        # try:
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
            f1, acc, mean = evaluate_loss(now_y_test, y_hat)
            score.append(1 - mean)
        mean_loss = np.mean(score)

        self.recorder.update(mean_loss, config)
        return {
            "loss": mean_loss,
            "info": {"config": config, "budget": budget},
        }


class Trainer:
    def __init__(self):
        self.config_parser = ConfigParser()
        self.recorder = Recorder()
        self.best_model = None
        self.best_loss = {}

    def train(self, X, y, col_names, n_worker=1, n_iter=20):
        k = 5
        logging.info("[trainer] start data division")
        division = []
        for i in range(k - 1):
            X_rest, X_part, y_rest, y_part = train_test_split(X, y, test_size=1 / (k - i),  stratify=y)
            division.append([X_part, y_part])
            X = X_rest
            y = y_rest
        division.append([X, y])

        # HPO using 4 divisions
        # one division for hold-out

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

        # first evaluate model with hold-out
        temp_best_model = ModelRunner(
            **self.config_parser.bohb_config2model_runner(self.recorder.best_config)
        )
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
        f1, acc, _ = evaluate_loss(y_test, y_hat)
        self.best_loss = f1

        # save best_model with full data

        logging.info("[trainer] save best model")
        self.best_model = ModelRunner(**self.config_parser.bohb_config2model_runner(self.recorder.best_config))
        self.best_model.train(X, y, col_names)

    def report(self):
        return {
            "best_config": self.best_model.get_config(),
            "evaluate": self.best_loss,
            "feature_importance": self.best_model.get_model().feature_importance(),
        }
