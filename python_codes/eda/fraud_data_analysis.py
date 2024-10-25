import numpy as np
import json
import os
from tqdm import tqdm
from util import preprocess_card, preprocess_user, NpEncoder

'''
distribution analysis of fraud data
'''

def analyze_distribution(df):
    '''
    :param df: pandas dataframe
    :return: distribution data of each column
    :description: check the type of column and get distribution data.
    for numeric column with the number of unique value bigger than 30 : histogram and min, mean, max
    for categorical column : percentage of each unique value
    '''
    data_distributions = []
    for col_name in df.columns:
        col = df[col_name]

        if col_name in ["Amount", "Per Capita Income - Zipcode","Yearly Income - Person","Total Debt","FICO Score","Credit Limit"]:
            col_type = "numeric"
            col = col.apply(lambda v: -1 if np.isnan(v) else v)
        else:
            col_type = "categorical"
        unique_values = col.unique()
        if len(unique_values) < 30:
            col_type = "categorical"
        if col_type == "numeric":
            # minmax, mean, histogram
            min = col.min()
            max = col.max()
            mean = col.mean()

            counts, bin_edges = np.histogram(col, bins=12)
            distribution_data = {
                "minmax": {
                    "min": min,
                    "max": max,
                    "mean": mean
                },
                "histogram": {
                    "counts": counts,
                    "bins": list(map(lambda num: num.round(4), bin_edges))
                }
            }
        elif col_type == "categorical":
            value_percentage = col.value_counts(normalize=True).round(4) * 100

            value_percentage_json = value_percentage.to_dict()
            distribution_data = {
                "value_percentage": []
            }
            for k, v in value_percentage_json.items():
                distribution_data["value_percentage"].append({
                    "name": str(k),
                    "value": v
                })
        else:
            distribution_data = []

        data_distributions.append({
            "col_name": col_name,
            "col_type": col_type,
            "distribution": distribution_data
        })
    return data_distributions

def load_df(df, user_df, card_df):
    df = pd.merge(df, user_df, left_on="User", right_on="id", how="left")
    df = pd.merge(df, card_df, left_on=["User", "Card"], right_on=["User", "CARD INDEX"], how="left")

    columns_to_drop = [
        "Errors?", "Is Fraud?", "User", "Card", "id", "CARD INDEX"
    ]
    df = df.drop(columns_to_drop, axis=1)
    df["Time"] = df["Time"].apply(lambda t: t.split(":")[0])
    df["Amount"] = df["Amount"].apply(lambda amount: amount[1:]).astype(float)

    return df


fraud_df = pd.read_csv("../data/processed/fraud_cases.csv")
user_df = preprocess_user(pd.read_csv("../data/processed/sd254_users_with_id.csv"))
card_df = preprocess_card(pd.read_csv("../data/given/sd254_cards.csv"))
not_fraud_chunks = []
result_path = "results/whole"
os.makedirs(result_path, exist_ok = True)
chunk_size = 100000

for chunk in tqdm(pd.read_csv("../data/processed/not_fraud_cases.csv", chunksize=chunk_size), desc="reading not fraud data"):
    # Sample 2% of rows from the current chunk
    sampled_chunk = chunk.sample(frac=0.02, random_state=6541)
    not_fraud_chunks.append(sampled_chunk)

not_fraud_df = pd.concat(not_fraud_chunks, ignore_index=True)

print("fraud")
fraud_data_dist = analyze_distribution(load_df(fraud_df, user_df, card_df))
with open(f"{result_path}/fraud_data_dist.json", "w") as f:
    json.dump(fraud_data_dist, f, cls=NpEncoder, indent=4)

print("not_fraud")
not_fraud_data_dist = analyze_distribution(load_df(not_fraud_df, user_df, card_df))
with open(f"{result_path}/not_fraud_data_dist.json", "w") as f:
    json.dump(not_fraud_data_dist, f, cls=NpEncoder, indent=4)

