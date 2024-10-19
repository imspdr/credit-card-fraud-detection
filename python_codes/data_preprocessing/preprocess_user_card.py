import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

'''
USER FEATURES
'''

user_df = pd.read_csv("../data/given/sd254_users.csv")

user_columns_to_use = [
    "Current Age", "Gender", "Zipcode", "Latitude", "Longitude", "Per Capita Income - Zipcode", "Yearly Income - Person", "Total Debt", "FICO Score", "Num Credit Cards"
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
    user_df[col] = user_df[col].apply(lambda val: val[1:]).astype(int)

user_df.to_csv("../data/processed/processed_user.csv", index=False)

'''
CARD FEATURES
'''
card_df = pd.read_csv("../data/given/sd254_cards.csv")

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
card_df["Credit Limit"] = card_df["Credit Limit"].apply(lambda limit: limit[1:]).astype(int)

card_df.to_csv("../data/processed/processed_card.csv", index=False)
