import pandas as pd
import numpy as np
import json

from python_codes.model.train.preprocess_user_card import preprocess_user, preprocess_card
from python_codes.util import NpEncoder
from python_codes.model.train.preprocessing import preprocessing
from python_codes.model.train.add_fraud_one_hot import add_fraud_one_hot
from python_codes.model.train.random_forest_classifier import CustomRandomForestClassifier
from python_codes.model.train.preprocess_user_card import *

'''
check feature importance of random forest classifier per user.
to find which column is important for representing fraud case.
'''

chunk_size = 100000
train_file = "../data/processed/train_transactions.csv"

temp_df = None

def get_top3_importance(feature_importance):
    top_values = [(0, 0)]
    for i, value in enumerate(feature_importance["value"]):
        if np.isnan(value):
            return None
        else:
            if top_values[0][1] < value:
                top_values.append((i, value))
                top_values.sort(key=lambda v: v[1])
                if len(top_values) > 3:
                    top_values.pop(0)
    return list(map(lambda tv: (feature_importance["label"][tv[0]], feature_importance["value"][tv[0]]), top_values))


# load data
report = {
    "top1": {},
    "top2": {},
    "top3": {}
}
user_df = preprocess_user(pd.read_csv("../data/processed/sd254_users_with_id.csv"))
card_df = preprocess_card(pd.read_csv("../data/given/sd254_cards.csv"))



# read train file chunk by chunk and train simple model for each user data
for chunk in pd.read_csv(train_file, chunksize=chunk_size):
    chunk_group = chunk.groupby(["User", "Card"]);

    for i, (user, df) in enumerate(chunk_group):
        print(f"now processing user : {user}")
        if i == 0:
            if temp_df and temp_df[0] == user:
                print(f"temp data from prev chunk checked. concat it")
                df = pd.concat([temp_df[1], df], ignore_index=True)
        if i == len(chunk_group) - 1:
            temp_df = (user, df)
            continue
        # select y
        target="Is Fraud?"
        y = df[target].apply(lambda fraud: 1 if fraud == "Yes" else 0).to_numpy()

        # preprocessing data
        df = preprocessing(df, card_df, user_df)
        df = add_fraud_one_hot(df)
        df = df.drop(["City", "Merchant City"], axis=1)

        # Train
        model = CustomRandomForestClassifier(n_estimators=100)
        model.fit(df.to_numpy(), y, list(df.columns))

        # save info
        top_fi = get_top3_importance(model.feature_importance())
        if top_fi and len(top_fi) > 2:
            print(f"report appended for user {user}")
            for k, fi in enumerate(top_fi):
                report_now = report[f"top{3-k}"]
                if fi[0] in report_now.keys():
                    report_now[fi[0]] += 1
                else:
                    report_now[fi[0]] = 1


with open(f"fi_report2.json", "w") as f:
    json.dump(report, f, cls=NpEncoder, indent=2)