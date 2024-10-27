import numpy as np
import pandas as pd
import json
import os
from tqdm import tqdm
from util import preprocess_card, preprocess_user, NpEncoder

'''
distribution analysis of fraud data
'''

def analyze_distribution(df, dist, histo_bins=None):
    '''
    :param df: pandas dataframe
    :return: distribution data of each column
    :description: check the type of column and get distribution data.
    for numeric column with the number of unique value bigger than 30 : histogram and min, mean, max
    for categorical column : percentage of each unique value
    '''
    for col_name in df.columns:
        col = df[col_name]
        if col_name in ["Amount",
                        "Per Capita Income - Zipcode",
                        "Yearly Income - Person",
                        "Current Age",
                        "Total Debt",
                        "FICO Score",
                        "Credit Limit"]:
            col_type = "numeric"
            col = col.apply(lambda v: -1 if np.isnan(v) else v)
        else:
            col_type = "categorical"

        if col_type == "numeric":
            additive = False

            min_val = col.min()
            max_val = col.max()
            sum_val = col.sum()
            len_val = len(col)

            for prev_dist in dist:
                if prev_dist["col_name"] == col_name:
                    counts, bin_edges = np.histogram(col, bins=prev_dist["distribution"]["histogram"]["bins"])
                    distribution_data = {
                        "minmax": {
                            "min": min(prev_dist["distribution"]["minmax"]["min"], min_val),
                            "max": max(prev_dist["distribution"]["minmax"]["max"], max_val),
                            "sum": prev_dist["distribution"]["minmax"]["sum"] + sum_val,
                            "len": prev_dist["distribution"]["minmax"]["len"] + len_val
                        },
                        "histogram": {
                            "counts": counts + prev_dist["distribution"]["histogram"]["counts"],
                            "bins": bin_edges
                        }
                    }
                    prev_dist["distribution"] = distribution_data
                    additive = True
                    break

            if not additive:
                bins = None
                if col_name == "Amount":
                    bins = [-1000,0,100,200,300,400,500,600,700,20000]
                if histo_bins:
                    for bins_info in histo_bins:
                        if bins_info["col_name"] == col_name:
                            bins = bins_info["bins"]
                            break
                counts, bin_edges = np.histogram(col, bins=bins if bins else 12)
                distribution_data = {
                    "minmax": {
                        "min": min_val,
                        "max": max_val,
                        "sum": sum_val,
                        "len": len_val
                    },
                    "histogram": {
                        "counts": counts,
                        "bins": list(map(lambda num: num.round(4), bin_edges))
                    }
                }
                dist.append({
                    "col_name": col_name,
                    "col_type": col_type,
                    "distribution": distribution_data
                })
        elif col_type == "categorical":
            additive = False
            value_count = col.value_counts()
            value_count_json = value_count.to_dict()
            for prev_dist in dist:
                if prev_dist["col_name"] == col_name:
                    for k, v in value_count_json.items():
                        already_exist = False
                        for item in prev_dist["distribution"]["value_count"]:
                            if item["name"] == str(k):
                                item["value"] += v
                                already_exist = True
                        if not already_exist:
                            prev_dist["distribution"]["value_count"].append(
                                {
                                    "name": str(k),
                                    "value": v
                                }
                            )

                    additive = True
            if not additive:
                distribution_data = {
                    "value_count": []
                }
                for k, v in value_count_json.items():
                    distribution_data["value_count"].append({
                        "name": str(k),
                        "value": v
                    })
                dist.append({
                    "col_name": col_name,
                    "col_type": col_type,
                    "distribution": distribution_data
                })
    return dist

def load_df(df, user_df, card_df):
    df = pd.merge(df, user_df, left_on="User", right_on="id", how="left")
    df = pd.merge(df, card_df, left_on=["User", "Card"], right_on=["User", "CARD INDEX"], how="left")

    columns_to_drop = [
        "Is Fraud?", "User", "Card", "id", "CARD INDEX", "Merchant Name"
    ]
    df = df.drop(columns_to_drop, axis=1)
    df["Time"] = df["Time"].apply(lambda t: t.split(":")[0])
    df["Amount"] = df["Amount"].apply(lambda amount: amount[1:]).astype(float)

    return df


fraud_df = pd.read_csv("../data/processed/fraud_cases.csv")
user_df = preprocess_user(pd.read_csv("../data/processed/sd254_users_with_id.csv"))
card_df = preprocess_card(pd.read_csv("../data/given/sd254_cards.csv"))

result_path = "results/whole"
os.makedirs(result_path, exist_ok = True)
chunk_size = 100000


print("fraud")
fraud_data_dist = analyze_distribution(load_df(fraud_df, user_df, card_df), [])
with open(f"{result_path}/fraud_data_dist.json", "w") as f:
    json.dump(fraud_data_dist, f, cls=NpEncoder, indent=4)


print("not_fraud")
fraud_histo_bins = list(map(
    lambda dist: {
        "col_name": dist["col_name"],
        "bins": dist["distribution"]["histogram"]["bins"]
    },
    filter(lambda dist: dist["col_type"] == "numeric", fraud_data_dist)
))
not_fraud_data_dist = []

for chunk in tqdm(pd.read_csv("../data/processed/not_fraud_cases.csv", chunksize=chunk_size), desc="reading not fraud data"):
    not_fraud_data_dist = analyze_distribution(
        load_df(chunk, user_df, card_df),
        not_fraud_data_dist,
        fraud_histo_bins
    )

with open(f"{result_path}/not_fraud_data_dist.json", "w") as f:
    json.dump(not_fraud_data_dist, f, cls=NpEncoder, indent=4)

