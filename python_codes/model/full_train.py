import pandas as pd
import json
import pickle
import os
from python_codes.util import NpEncoder
from python_codes.model.train.preprocessing import preprocessing
from python_codes.model.train.add_fraud_one_hot import add_fraud_one_hot
from python_codes.model.train.random_forest_classifier import CustomRandomForestClassifier


chunk_size = 100000
custom_model = CustomRandomForestClassifier()
train_file = "../data/processed/train_transactions.csv"
result_path = "results/full_train"
os.makedirs(result_path, exist_ok=True)


for i, df in enumerate(pd.read_csv(train_file, chunksize=chunk_size)):
    # select y
    target="Is Fraud?"
    y = df[target].apply(lambda fraud: 1 if fraud == "Yes" else 0).to_numpy()

    print(f"training {i}th chunk")
    df = preprocessing(df)
    df = add_fraud_one_hot(df)
    custom_model.fit(df.to_numpy(), y, list(df.columns))

fi = custom_model.feature_importance()

with open(f"{result_path}/report.json", "w") as f:
    json.dump(fi, f, cls=NpEncoder, indent=4)
with open(f"{result_path}/rf_full_train_model.pkl", "wb") as pkl_file:
    pickle.dump(custom_model, pkl_file)