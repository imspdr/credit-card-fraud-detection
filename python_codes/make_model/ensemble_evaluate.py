import pickle
import pandas as pd
import numpy as np
from model.feature_engineering.preprocess_user_card import preprocess_user, preprocess_card
from model.feature_engineering.generate_user_feature import generate_user_feature
from model.feature_engineering.preprocessing import preprocessing
from model.feature_engineering.generate_age_feature import generate_age_feature
from model.feature_engineering.add_fraud_one_hot import add_fraud_one_hot
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
df = generate_age_feature(df)
df = add_fraud_one_hot(df)
df = generate_user_feature(df)

# load model
with open(f"{result_path}/ensemble_model.pkl", "rb") as pkl_file:
    now_model = pickle.load(pkl_file)

# do inference with each model
result = []
for i, model in tqdm(enumerate(now_model), desc=f"inference using each model in ensemble"):
    y_hat = model.inference_proba(df.to_numpy())
    result.append(y_hat)

y_hats_array = np.array(result)

# get mean of data
mean_y_hat = np.mean(y_hats_array, axis=0)

thresholds = np.arange(0.1, 1.0, 0.05)
f1_scores = []
recalls = []
precisions = []

# for each threshold get result
for threshold in thresholds:
    final_result = (mean_y_hat >= threshold).astype(int)
    f1 = f1_score(y_true, final_result)
    recall = recall_score(y_true, final_result)
    precision = precision_score(y_true, final_result)

    f1_scores.append(f1)
    recalls.append(recall)
    precisions.append(precision)
    print(f"with threshold {threshold} ")
    print(f"recall : {recall}")
    print(f"precision : {precision}")
    print(f"f1 : {f1}")
    print(classification_report(y_true, final_result))



import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(thresholds, f1_scores, label='F1 Score', marker='o')
plt.plot(thresholds, precisions, label='Precision', marker='o')
plt.plot(thresholds, recalls, label='Recall', marker='o')

plt.xlabel('Threshold')
plt.ylabel('Score')
plt.legend(loc='best')
plt.grid(True)
plt.show()