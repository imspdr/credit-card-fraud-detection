import pandas as pd
from tqdm import tqdm

fraud_rows = []

chunk_size = 100000
header_flag = True
csv_file = "../data/processed/train_transactions.csv"
not_froud_file = "../data/processed/not_fraud_cases.csv"
for chunk in tqdm(pd.read_csv(csv_file, chunksize=chunk_size), desc="reading train transaction file and get fraud data"):
    fraud_chunk = chunk[chunk["Is Fraud?"] == "Yes"]
    not_froud_chunk = chunk[chunk["Is Fraud?"] == "No"]
    fraud_rows.append(fraud_chunk)

    not_froud_chunk.to_csv(
        not_froud_file, mode='a', index=False, header=header_flag
    )
    header_flag = False

fraud_data = pd.concat(fraud_rows, ignore_index=True)

fraud_data.to_csv("../data/processed/fraud_cases.csv", index=False)