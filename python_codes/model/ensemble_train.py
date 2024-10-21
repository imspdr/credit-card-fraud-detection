import pandas as pd
import logging
import json
import pickle
from python_codes.util import NpEncoder
from preprocessing import preprocessing
from add_fraud_one_hot import add_fraud_one_hot
from python_codes.model.train.trainer import Trainer

logging.basicConfig(level=logging.INFO)

logging.info("load data")
chunk_size = 100000
not_fraud_file = "../data/processed/shuffled_not_fraud_cases.csv"
fraud_df = pd.read_csv("../data/processed/fraud_cases.csv")
ensemble = []

for i, df in enumerate(pd.read_csv(not_fraud_file, chunksize=chunk_size)):
    # select y
    df = pd.concat([df, fraud_df], ignore_index=True)

    target="Is Fraud?"
    y = df[target].apply(lambda fraud: 1 if fraud == "Yes" else 0).to_numpy()

    # preprocessing
    df = preprocessing(df)

    # add fraud feature one-hot encoding
    df = add_fraud_one_hot(df)

    # Train
    logging.info(f"train {i}th chunk")

    trainer = Trainer()
    trainer.train(df.to_numpy(), y, list(df.columns), n_iter=10)
    ensemble.append(trainer.best_model)

    report = trainer.report()
    with open(f"results/report{i}.json", "w") as f:
        json.dump(report, f, cls=NpEncoder, indent=4)

    if i>=10:
        break

with open(f"trained_model.pkl", "wb") as pkl_file:
    pickle.dump(ensemble, pkl_file)