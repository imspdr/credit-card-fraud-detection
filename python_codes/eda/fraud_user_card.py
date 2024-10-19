import pandas as pd
from python_codes.model.random_forest_classifier import CustomRandomForestClassifier

fraud_df = pd.read_csv("fraud_cases.csv")

fraud_user = []

for index, row in fraud_df.iterrows():
    now = (row["User"], row["Card"])
    if now not in fraud_user:
        fraud_user.append(now)

card_df = pd.read_csv("../data/processed/processed_card.csv")
user_df = pd.read_csv("../data/processed/processed_user.csv")
df = pd.merge(card_df, user_df, left_on="User", right_index=True, how="left")

y = []
for index, row in df.iterrows():
    now = (row["User"], row["CARD INDEX"])
    if now not in fraud_user:
        y.append(0)
    else:
        y.append(1)

rf = CustomRandomForestClassifier(n_estimators=100, max_features=0.8)

rf.fit(df.to_numpy(), y, list(df.columns))

fi = rf.feature_importance()
for i, value in enumerate(fi["value"]):
    print(fi["label"][i], value)
