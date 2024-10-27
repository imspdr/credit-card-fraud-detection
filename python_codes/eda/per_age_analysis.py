import json
import os
from tqdm import tqdm
import pandas as pd
from util import preprocess_user, NpEncoder

'''
get merchant name prefered from each age group
'''

user_df = preprocess_user(pd.read_csv("../data/processed/sd254_users_with_id.csv"))
result_path = "results/per_age"
os.makedirs(result_path, exist_ok = True)
chunk_size = 100000

bins = [0, 20, 40, 60, float('inf')]
labels = ["~20", "~40", "~60", "60+"]
def age_group(age):
    if age < 20:
        return "~20"
    elif age < 40:
        return "~40"
    elif age < 60:
        return "~60"
    else:
        return "60+"

# counts of the number of each group (111, 720, 723, 446)
user_df.loc[:, "age_group"] = user_df["Current Age"].apply(age_group)
for age_group, df in user_df.groupby("age_group"):
    print(age_group, len(df))

count_per_group = {}
for label in labels:
    count_per_group[label] = {}

for df in tqdm(pd.read_csv("../data/processed/not_fraud_cases.csv", chunksize=chunk_size), desc="reading data as chunk"):
    df = pd.merge(df, user_df, left_on="User", right_on="id", how="left")
    columns_to_use = [
        "User", "Amount", "Current Age", "Merchant Name", "age_group"
    ]
    df = df[columns_to_use]
    for (user, group, merchant), group_df in df.groupby(["User", "age_group", "Merchant Name"]):
        if merchant in count_per_group[group].keys():
            if user not in count_per_group[group][merchant]:
                count_per_group[group][merchant].append(user)
        else:
            count_per_group[group][merchant] = [user]

result = []
for group, value_dict in count_per_group.items():
    group_top10 = []
    for merchant, users in value_dict.items():
        group_top10.append((merchant, len(users)))
        group_top10.sort(key=lambda item:item[1])
        if len(group_top10) > 10:
            group_top10.pop(0)
    result.append({
        "group": group,
        "top10": group_top10
    })

with open(f"{result_path}/result.json", "w") as f:
    json.dump(result, f, cls=NpEncoder, indent=4)


