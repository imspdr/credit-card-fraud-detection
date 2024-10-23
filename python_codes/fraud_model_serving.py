import logging
import kserve
import json
import pickle
import pandas as pd
import numpy as np

from typing import Dict
from train.preprocessing import preprocessing
from train.add_fraud_one_hot import add_fraud_one_hot
from train.generate_user_feature import generate_user_feature
from train.preprocess_user_card import preprocess_card, preprocess_user

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
            df = pd.DataFrame(payload["transaction"])
            user_df = preprocess_user(pd.DataFrame(payload["user"]))
            card_df = preprocess_card(pd.DataFrame(payload["card"]))
            print(df)
            print(user_df)
            print(card_df)
            df = preprocessing(df, card_df, user_df)
            df = add_fraud_one_hot(df)
            df = generate_user_feature(df)

            result = []
            for i, model in enumerate(self.model):
                y_hat = model.inference(df.to_numpy())
                result.append(y_hat)
                print(f"{i}th model result")
                print(y_hat)

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