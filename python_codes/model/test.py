import pandas as pd
import logging
import json
import pickle
from python_codes.util import NpEncoder
from preprocessing import preprocessing
from add_fraud_one_hot import add_fraud_one_hot
from random_forest_classifier import CustomRandomForestClassifier

logging.basicConfig(level=logging.INFO)

logging.info("load data")
chunk_size = 100000
custom_model = CustomRandomForestClassifier()
train_file = "../data/processed/train_transactions.csv"

for i, df in enumerate(pd.read_csv(train_file, chunksize=chunk_size)):
    # select y
    target="Is Fraud?"
    y = df[target].apply(lambda fraud: 1 if fraud == "Yes" else 0).to_numpy()

    # preprocessing
    df = preprocessing(df)

    # add fraud feature one-hot encoding
    df = add_fraud_one_hot(df)

    # Train
    logging.info(f"train {i}th chunk")
    if i ==0:
        custom_model.fit(df.to_numpy(), y, list(df.columns))
    else:
        custom_model.additive_fit(df.to_numpy(), y)

fi = custom_model.feature_importance()

with open(f"report.json", "w") as f:
    json.dump(fi, f, cls=NpEncoder, indent=4)
with open(f"trained_model.pkl", "wb") as pkl_file:
    pickle.dump(custom_model, pkl_file)