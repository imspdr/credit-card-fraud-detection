import pandas as pd
import json
import pickle
import os
from tqdm import tqdm
from train.util import NpEncoder
from train.preprocessing import preprocessing
from train.add_fraud_one_hot import add_fraud_one_hot
from train.generate_user_feature import generate_user_feature
from train.random_forest_classifier import CustomRandomForestClassifier
from train.preprocess_user_card import preprocess_user, preprocess_card

'''
Train random forest with full data
load train data chunk by chunk and do additive train
'''
chunk_size = 100000
custom_model = CustomRandomForestClassifier(n_estimators=10, max_features=0.8)
train_file = "../data/processed/train_transactions.csv"
result_path = "results/full_train"
user_df = preprocess_user(pd.read_csv("../data/processed/sd254_users_with_id.csv"))
card_df = preprocess_card(pd.read_csv("../data/given/sd254_cards.csv"))

os.makedirs(result_path, exist_ok=True)

# train
for i, df in tqdm(enumerate(pd.read_csv(train_file, chunksize=chunk_size)), desc="training rf"):
    # select y
    target="Is Fraud?"
    y = df[target].apply(lambda fraud: 1 if fraud == "Yes" else 0).to_numpy()

    # preprocessing
    df = preprocessing(df, card_df, user_df)
    df = add_fraud_one_hot(df)
    df = generate_user_feature(df)

    if i == 0:
        custom_model.fit(df.to_numpy(), y, list(df.columns))
    else:
        custom_model.additive_fit(df.to_numpy(), y)

fi = custom_model.feature_importance()

with open(f"{result_path}/report.json", "w") as f:
    json.dump(fi, f, cls=NpEncoder, indent=4)
with open(f"{result_path}/rf_full_train_model.pkl", "wb") as pkl_file:
    pickle.dump(custom_model, pkl_file)