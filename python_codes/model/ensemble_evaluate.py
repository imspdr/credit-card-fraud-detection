import pickle
import pandas as pd
import numpy as np
import logging
from python_codes.model.train.preprocessing import preprocessing
from python_codes.model.train.add_fraud_one_hot import add_fraud_one_hot
from python_codes.model.train.generate_user_feature import generate_user_feature
from sklearn.metrics import classification_report, f1_score
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

df = pd.read_csv("../data/processed/hold_out_transactions.csv")
user_df = pd.read_csv("../data/processed/processed_user.csv")
card_df = pd.read_csv("../data/processed/processed_card.csv")
target = "Is Fraud?"
y_true = df[target].apply(lambda fraud: 1 if fraud == "Yes" else 0).to_numpy()
result_path = "results/ensemble_train"


df = preprocessing(df, card_df, user_df)
df = add_fraud_one_hot(df)
df = generate_user_feature(df)

with open(f"{result_path}/ensemble_model.pkl", "rb") as pkl_file:
    now_model = pickle.load(pkl_file)

result = []
for i, model in tqdm(enumerate(now_model), desc=f"inference using each model in ensemble"):
    y_hat = model.inference(df.to_numpy())
    result.append(y_hat)

y_hats_array = np.array(result)

# Step 2: Calculate the mean of predictions along axis=0 (column-wise)
mean_y_hat = np.mean(y_hats_array, axis=0)

# Step 3: Apply the condition: Set 1 if mean > 0.5 else 0
final_result = (mean_y_hat >= 0.3).astype(int)
print(f1_score(y_true, final_result, average="weighted"))
print(classification_report(y_true, final_result))
