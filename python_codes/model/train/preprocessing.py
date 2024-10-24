import pandas as pd

def preprocessing(df: pd.DataFrame, card_df: pd.DataFrame, user_df: pd.DataFrame) -> pd.DataFrame:
    columns_to_use = ["User", "Card", "Time", "Amount", "Use Chip", "Merchant Name", "Merchant City", "Merchant State", "Zip", "MCC"]
    # 0. select columns
    df = df[columns_to_use]

    # 1. Time - remove minute
    df.loc[:, "Time"] = df["Time"].apply(lambda t: t.split(":")[0]).astype(int)

    # 2. Amount - remove dollar sign
    df.loc[:, "Amount"] = df["Amount"].apply(lambda amount: amount[1:]).astype(float)

    # 3. Merge user info
    user_merged_df = pd.merge(df, user_df, left_on="User", right_on="id", how="left")

    # 4. Merge Card info
    card_merged_df = pd.merge(user_merged_df, card_df, left_on=["User", "Card"], right_on=["User", "CARD INDEX"], how="left")

    last_df = card_merged_df.drop(["User", "Card", "id", "CARD INDEX"], axis=1)

    return last_df