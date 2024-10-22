import pandas as pd
from tqdm import tqdm

'''
divide hold-out data set for last evaluation (user 1990 ~ )
load transaction data chunk by chunk and save csv for each chunk
'''

chunk_size = 100000
header_flag = True

csv_file = "../data/given/credit_card_transactions-ibm_v2.csv"
holdout_path = "../data/processed/hold_out_transactions.csv"
train_path = "../data/processed/train_transactions.csv"
for chunk in tqdm(pd.read_csv(csv_file, chunksize=chunk_size), desc="reading transaction file and divide it to hold-out and train"):
    # Split the chunk into hold-out (user_id 1990 ~ 1999) and train set (user_id 0 ~ 1989)
    holdout_chunk = chunk[chunk["User"] >1989]
    train_chunk = chunk[chunk["User"] <=1989]

    holdout_chunk.to_csv(
        holdout_path, mode='a', index=False, header=header_flag
    )
    train_chunk.to_csv(
        train_path, mode='a', index=False, header=header_flag
    )
    header_flag = False
