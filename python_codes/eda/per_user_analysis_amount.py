import pandas as pd
import json

import matplotlib.pyplot as plt
from python_codes.model.preprocessing import preprocessing
from python_codes.util import NpEncoder

chunk_size = 100000
not_fraud_file = "not_fraud_cases.csv"
fraud_df = pd.read_csv("fraud_cases.csv")

temp_df = None

report = []
for chunk in pd.read_csv(not_fraud_file, chunksize=chunk_size):
    chunk_group = chunk.groupby("User");

    for i, (user, df) in enumerate(chunk_group):
        print(f"now processing user : {user}")
        if i == 0:
            if temp_df and temp_df[0] == user:
                print(f"temp data from prev chunk checked. concat it")
                df = pd.concat([temp_df[1], df], ignore_index=True)
        if i == len(chunk_group) - 1:
            temp_df = (user, df)
            continue
        df = preprocessing(df)

        user_mean = df.groupby("Time").agg(
            mean_amount=("Amount", "mean"),
            transaction_count=("Amount", "count")
        ).reset_index()

        user_fraud = fraud_df[fraud_df.apply(lambda row: row["User"] == user, axis=1)]
        user_fraud = preprocessing(user_fraud)
        user_fraud = user_fraud[["Time", "Amount"]]

        report.append(
            {
                "user": user,
                "data": user_mean.to_json(orient="records"),
                "fraud": user_fraud.to_json(orient="records")
            }
        )


    break

with open(f"amount_report.json", "w") as f:
    json.dump(report, f, cls=NpEncoder, indent=2)