import pandas as pd

chunk_size = 10000
fraud_rows = []

csv_file = 'credit_card_transactions-ibm_v2.csv'
for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
    fraud_chunk = chunk[chunk["Is Fraud?"] == 'Yes']
    fraud_rows.append(fraud_chunk)

result = pd.concat(fraud_rows, ignore_index=True)

result.to_csv('fraud_cases.csv', index=False)