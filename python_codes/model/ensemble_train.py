import pandas as pd
import logging
import json
import pickle
import os

from python_codes.model.train.generate_user_feature import generate_user_feature
from python_codes.util import NpEncoder
from python_codes.model.train.preprocessing import preprocessing
from python_codes.model.train.add_fraud_one_hot import add_fraud_one_hot
from python_codes.model.train.trainer import Trainer

logging.basicConfig(level=logging.INFO)

logging.info("load data")
chunk_size = 100000
not_fraud_file = "../data/processed/shuffled_not_fraud_cases.csv"
fraud_df = pd.read_csv("../data/processed/fraud_cases.csv")
user_df = pd.read_csv("../data/processed/processed_user.csv")
card_df = pd.read_csv("../data/processed/processed_card.csv")
ensemble = []
whole_report = []
result_path = "results/ensemble_train"
os.makedirs(result_path, exist_ok=True)

for i, df in enumerate(pd.read_csv(not_fraud_file, chunksize=chunk_size)):
    # select y
    df = pd.concat([df, fraud_df], ignore_index=True)

    target="Is Fraud?"
    y = df[target].apply(lambda fraud: 1 if fraud == "Yes" else 0).to_numpy()

    # preprocessing
    df = preprocessing(df, card_df, user_df)
    df = add_fraud_one_hot(df)
    df = generate_user_feature(df)

    # Train
    logging.info(f"train {i}th chunk")

    trainer = Trainer()
    now_model = trainer.train_with_hpo(df.to_numpy(), y, list(df.columns), n_iter=10)
    report = trainer.report()

    ensemble.append(now_model)

    whole_report.append({
        "index": i,
        "data": report
    })
    if i >= 9:
        break

with open(f"{result_path}/report.json", "w") as f:
    json.dump(whole_report, f, cls=NpEncoder, indent=4)
with open(f"{result_path}/ensemble_model.pkl", "wb") as pkl_file:
    pickle.dump(ensemble, pkl_file)