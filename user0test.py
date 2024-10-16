import pandas as pd

'''
USER FEATURES
'''

user_df = pd.read_csv("sd254_users.csv")

user_columns_to_use = [
    "Current Age", "Gender", "Zipcode", "Per Capita Income - Zipcode", "Yearly Income - Person", "Total Debt", "FICO Score", "Num Credit Cards"
]

# 0. select column
user_df = user_df[user_columns_to_use]

# 1. Gender to int (male = 1, female = 0)
user_df["Gender"] = user_df["Gender"].apply(lambda male: 1 if male == "Male" else 0)

# 2. remove dollar sign
dollar_columns = [
    "Per Capita Income - Zipcode", "Yearly Income - Person", "Total Debt"
]

for col in dollar_columns:
    user_df[col] = user_df[col].apply(lambda val: val[1:])

'''
CARD FEATURES
'''
card_df = pd.read_csv("sd254_cards.csv")

card_columns_to_use = [
    "User", "CARD INDEX", "Card Type", "Has Chip", "Cards Issued", "Credit Limit", "Year PIN last Changed"
]

# 0. select column
card_df = card_df[card_columns_to_use]

# 1. Card Type to int (Credit = 1 , Debit = 0)
card_df["Card Type"] = card_df["Card Type"].apply(lambda card_type: 1 if card_type == "Credit" else 0)

# 2. Has Chip to int (YES = 1, NO = 0)
card_df["Has Chip"] = card_df["Has Chip"].apply(lambda has_chip: 1 if has_chip == "YES" else 0)

# 3. Limit remove dollar sign
card_df["Credit Limit"] = card_df["Credit Limit"].apply(lambda limit: limit[1:])


'''
CONCAT TRANSACTION
'''

df = pd.read_csv("User0_credit_card_transactions.csv")

columns_to_use = [
    "User", "Card", "Year", "Month", "Day", "Time", "Amount", "Use Chip", "Zip", "MCC"
]

# 0. select and labeling target
target = df.columns[-1]
y = df[target].apply(lambda fraud: 1 if fraud == "Yes" else 0).to_numpy()

df = df[columns_to_use]

# 1. Time - remove minute
df["Time"] = df["Time"].apply(lambda t: t.split(":")[0])

# 2. Amount - remove dollar sign
df["Amount"] = df["Amount"].apply(lambda amount: amount[1:])

# 3. Use Chip - online = 1
df["Use Chip"] = df["Use Chip"].apply(lambda chip: 1 if chip == "Online Transaction" else 0)

# 4. Append user info from User
user_merged_df = pd.merge(df, user_df, left_on="User", right_index=True, how="left")

# 5. Append Card info from User and Card
card_merged_df = pd.merge(user_merged_df, card_df, left_on=["User", "Card"], right_on=["User", "CARD INDEX"], how="left")

last_df = card_merged_df.drop(["User", "Card", "CARD INDEX"], axis=1)


'''
TRAIN MODEL with data
'''
col_names = list(last_df.columns)
X = last_df.to_numpy()

from train.trainer import Trainer

trainer = Trainer()
trainer.train(X, y, col_names=col_names)
report = trainer.report()
fi = report["feature_importance"]
for i, label in enumerate(fi["label"]):
    print(label, fi["value"][i])