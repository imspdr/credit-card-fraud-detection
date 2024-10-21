import pandas as pd

def preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_drop = [
        "Year", "Month", "Day", "Merchant City", "Errors?", "Is Fraud?"
    ]
    # 0. select columns
    df = df.drop(columns_to_drop, axis=1)

    # 1. Time - remove minute
    df.loc[:, "Time"] = df["Time"].apply(lambda t: t.split(":")[0]).astype(int)

    # 2. Amount - remove dollar sign
    df.loc[:, "Amount"] = df["Amount"].apply(lambda amount: amount[1:]).astype(float)

    # 3. Append user info from User
    user_df = pd.read_csv("../data/processed/processed_user.csv")
    user_merged_df = pd.merge(df, user_df, left_on="User", right_index=True, how="left")

    # 4. Append Card info from User and Card
    card_df = pd.read_csv("../data/processed/processed_card.csv")
    card_merged_df = pd.merge(user_merged_df, card_df, left_on=["User", "Card"], right_on=["User", "CARD INDEX"], how="left")

    last_df = card_merged_df.drop(["Longitude", "Latitude", "User", "Card", "CARD INDEX"], axis=1)

    return last_df