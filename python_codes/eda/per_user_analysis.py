import json
import os
import pandas as pd

from util import preprocess_card, preprocess_user, NpEncoder

'''
distribution analysis per user for Time, Amount, Merchant Name
'''

def user_analysis(fraud, not_fraud):
    time_data = []

    for i in range(24):
        k = f"0{i}" if i < 10 else f"{i}"
        time_fraud = fraud[fraud["Time"] == k]
        time_not_fraud = not_fraud[not_fraud["Time"] == k]
        fraud_count = len(time_fraud)
        not_fraud_count = len(time_not_fraud)
        time_data.append({
            "time": str(k),
            "not_fraud_count": not_fraud_count,
            "fraud_count": fraud_count,
        })

    return time_data

train_file = "../data/processed/train_transactions.csv"
result_path = "results/peruser"
chunk_size = 100000

temp_df = None

os.makedirs(result_path, exist_ok = True)

report = []

card_df = preprocess_card(pd.read_csv("../data/given/sd254_cards.csv"))
user_df = preprocess_user(pd.read_csv("../data/processed/sd254_users_with_id.csv"))

# read train file chunk by chunk and train simple model for each user data
for chunk in pd.read_csv(train_file, chunksize=chunk_size):
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
        df = pd.merge(df, user_df, left_on="User", right_on="id", how="left")
        columns_to_use = [
            "Time", "Amount", "Yearly Income - Person", "Total Debt", "Is Fraud?"
        ]

        df = df[columns_to_use]
        df["Time"] = df["Time"].apply(lambda t: t.split(":")[0])
        df["Amount"] = df["Amount"].apply(lambda amount: amount[1:]).astype(float)
        fraud_df = df[df["Is Fraud?"] == "Yes"]
        not_fraud_df = df[df["Is Fraud?"] == "No"]
        if not len(fraud_df) > 0:
            continue
        report.append({
            "user": user,
            "total_debt": df["Total Debt"][0],
            "yearly_income": df["Yearly Income - Person"][0],
            "time_data": user_analysis(fraud_df, not_fraud_df)
        })

    if user > 200:
        break

with open(f"{result_path}/data_dists.json", "w") as f:
    json.dump(report, f, cls=NpEncoder, indent=4)
