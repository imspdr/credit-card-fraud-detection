import logging
import kserve
import json
import pickle
import pandas as pd
import numpy as np

from typing import Dict
from model.feature_engineering.preprocess_user_card import preprocess_user, preprocess_card
from model.feature_engineering.generate_user_feature import generate_user_feature
from model.feature_engineering.preprocessing import preprocessing
from model.feature_engineering.generate_age_feature import generate_age_feature
from model.feature_engineering.add_fraud_one_hot import add_fraud_one_hot

def try_or_default(dict, key, default_value):
    try:
        ret = dict[key]
    except KeyError:
        ret = default_value
    return ret

def is_number(v):
    try:
        float(v)
        return True
    except (ValueError, TypeError):
        return False

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        else:
            return super(NpEncoder, self).default(obj)

class FraudServing(kserve.Model):
    def __init__(self, name):
        super().__init__(name)
        self.ready = False
        self.model_name = name
        self.model = None

    def load(self) -> bool:
        # load model
        with open("ensemble_model.pkl", "rb") as pkl_file:
            model = pickle.load(pkl_file)
        self.model = model
        self.ready = True
        return self.ready

    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        try:
            logging.info("[predictor] start serving")
            df = pd.DataFrame(payload["transaction"])
            user_df = preprocess_user(pd.DataFrame(payload["user"]))
            card_df = preprocess_card(pd.DataFrame(payload["card"]))

            logging.info(f"[predictor] successfully read request data length : {len(df)}")
            df = preprocessing(df, card_df, user_df)
            df = generate_age_feature(df)
            df = add_fraud_one_hot(df)
            df = generate_user_feature(df)

            logging.info("[predictor] successfully done feature engineering")
            result = []


            logging.info("[predictor] start prediction")
            for i, model in enumerate(self.model):
                y_hat = model.inference_proba(df.to_numpy())
                result.append(y_hat)

            logging.info("[predictor] prediction done")
            y_hats_array = np.array(result)
            mean_y_hat = np.mean(y_hats_array, axis=0)

            result = {
                "predictions": mean_y_hat,
            }
            json_result = json.dumps(obj=result, cls=NpEncoder, indent=4, ensure_ascii=False)
            return json.loads(json_result)

        except Exception as e:
            raise Exception("Failed to predict %s" % e)

if __name__ == "__main__":
    model = FraudServing("fraud-detection-serving")
    kserve.ModelServer().start([model])