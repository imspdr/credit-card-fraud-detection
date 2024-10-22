import pickle
import pandas as pd
import numpy as np
from python_codes.model.train.preprocess_user_card import preprocess_user, preprocess_card
from python_codes.model.train.preprocessing import preprocessing
from python_codes.model.train.add_fraud_one_hot import add_fraud_one_hot
from python_codes.model.train.generate_user_feature import generate_user_feature
from sklearn.metrics import classification_report, f1_score, recall_score, precision_score
from tqdm import tqdm

'''
evaluate ensemble model with hold-out dataset (user 1990~)
'''

df = pd.read_csv("../data/processed/eval_data.csv")
user_df = preprocess_user(pd.read_csv("../data/processed/sd254_users_with_id.csv"))
card_df = preprocess_card(pd.read_csv("../data/given/sd254_cards.csv"))
target = "Is Fraud?"
y_true = df[target].apply(lambda fraud: 1 if fraud == "Yes" else 0).to_numpy()
result_path = "results/ensemble_train"

# preprocessing
df = preprocessing(df, card_df, user_df)
df = add_fraud_one_hot(df)
df = generate_user_feature(df)

# load model
with open(f"{result_path}/ensemble_model.pkl", "rb") as pkl_file:
    now_model = pickle.load(pkl_file)

# do inference with each model
result = []
for i, model in tqdm(enumerate(now_model), desc=f"inference using each model in ensemble"):
    y_hat = model.inference(df.to_numpy())
    result.append(y_hat)

y_hats_array = np.array(result)

# get mean of data
mean_y_hat = np.mean(y_hats_array, axis=0)

# for each threshold get result
for threshold in range(1, 10):
    final_result = (mean_y_hat >= threshold / 10).astype(int)
    f1 = f1_score(y_true, final_result, average="weighted")
    recall = recall_score(y_true, final_result)
    precision = precision_score(y_true, final_result)

    print(f"with threshold {threshold / 10} ")
    print(f"recall : {recall}")
    print(f"precision : {precision}")
    print(f"weighted f1 : {f1}")
    print(classification_report(y_true, final_result))
