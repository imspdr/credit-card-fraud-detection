import json
import numpy as np
import pandas as pd

'''
select and preprocessing user and card feature
'''

'''
USER FEATURES
'''
def preprocess_user(user_df: pd.DataFrame) -> pd.DataFrame:
    # Columns to drop. do not use personal info. and remove spatial info except City
    user_columns_to_drop = ["Person", "Retirement Age", "Birth Year", "Birth Month", "Address", "Apartment", "State", "Zipcode", "Latitude", "Longitude"]

    # 0. select column
    user_df = user_df.drop(user_columns_to_drop, axis=1)

    # 1. Gender to int (male = 1, female = 0)
    user_df["Gender"] = user_df["Gender"].apply(lambda male: 1 if male == "Male" else 0)

    # 2. remove dollar sign
    dollar_columns = [
        "Per Capita Income - Zipcode", "Yearly Income - Person", "Total Debt"
    ]

    for col in dollar_columns:
        user_df[col] = user_df[col].apply(lambda val: val[1:]).astype(int)

    return user_df

'''
CARD FEATURES
'''
def preprocess_card(card_df: pd.DataFrame) -> pd.DataFrame:
    # Columns to drop. drop card specific infos and "Card on Dark Web" because it has all false
    card_columns_to_drop = ["Card Brand", "Card Number", "Expires", "CVV", "Acct Open Date", "Card on Dark Web"]

    # 0. select column
    card_df = card_df.drop(card_columns_to_drop, axis=1)

    # 1. Card Type to int (Credit = 1 , Debit = 0)
    card_df["Card Type"] = card_df["Card Type"].apply(lambda card_type: 1 if card_type == "Credit" else 0)

    # 2. Has Chip to int (YES = 1, NO = 0)
    card_df["Has Chip"] = card_df["Has Chip"].apply(lambda has_chip: 1 if has_chip == "YES" else 0)

    # 3. Limit remove dollar sign
    card_df["Credit Limit"] = card_df["Credit Limit"].apply(lambda limit: limit[1:]).astype(int)

    return card_df

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        else:
            return super(NpEncoder, self).default(obj)