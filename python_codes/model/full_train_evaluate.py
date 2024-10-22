import pickle
import pandas as pd
import logging
from python_codes.model.train.preprocessing import preprocessing
from python_codes.model.train.add_fraud_one_hot import add_fraud_one_hot
from python_codes.model.train.generate_user_feature import generate_user_feature
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score

'''
evaluate full trained model with hold-out dataset (user 1990~)
'''

df = pd.read_csv("../data/processed/hold_out_transactions.csv")
user_df = pd.read_csv("../data/processed/processed_user.csv")
card_df = pd.read_csv("../data/processed/processed_card.csv")
target = "Is Fraud?"
y_true = df[target].apply(lambda fraud: 1 if fraud == "Yes" else 0).to_numpy()
result_path = "results/ensemble_train"

# preprocessing
df = preprocessing(df, card_df, user_df)
df = add_fraud_one_hot(df)
df = generate_user_feature(df)

with open(f"{result_path}/rf_full_train_model.pkl", "rb") as pkl_file:
    now_model = pickle.load(pkl_file)
y_hat = now_model.predict(df.to_numpy())

print(f1_score(y_true, y_hat))
print(classification_report(y_true, y_hat))
