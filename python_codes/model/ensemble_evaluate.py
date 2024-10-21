import pickle
import pandas as pd
import logging
from preprocessing import preprocessing
from add_fraud_one_hot import add_fraud_one_hot
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score

logging.basicConfig(level=logging.INFO)

df = pd.read_csv("../data/processed/hold_out_transactions.csv")
target = "Is Fraud?"
y_true = df[target].apply(lambda fraud: 1 if fraud == "Yes" else 0).to_numpy()

# preprocessing
logging.info("preprocessing")
df = preprocessing(df)

# add fraud feature one-hot encoding
logging.info("add fraud one hot columns")
df = add_fraud_one_hot(df)

with open(f"trained_model.pkl", "rb") as pkl_file:
    now_model = pickle.load(pkl_file)

for i, model in enumerate(now_model):

    y_hat = model.inference(df.to_numpy())
    print(i)
    print(f1_score(y_true, y_hat))
    print(classification_report(y_true, y_hat))
