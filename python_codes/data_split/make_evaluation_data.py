import pandas as pd

holdout_df = pd.read_csv("../data/processed/hold_out_transactions.csv")

holdout_fraud = holdout_df[holdout_df["Is Fraud?"] == "Yes"]
holdout_not_fraud = holdout_df[holdout_df["Is Fraud?"] == "No"].sample(n=len(holdout_fraud) * 3, random_state=6541)

pd.concat([holdout_not_fraud, holdout_fraud]).to_csv("../data/processed/eval_data.csv", index=False)

