import pandas as pd

def generate_user_feature(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Amount / Yearly Income - Person
    df.loc[:, "Amount / Income"] = df.apply(lambda row: row["Amount"] / max(row["Yearly Income - Person"], 1), axis=1)

    # 2. Amount / Card Credit Limit
    df.loc[:, "Amount / Credit Limit"] = df.apply(lambda row: row["Amount"] / max(row["Credit Limit"], 1), axis=1)

    # 3. Amount / Total Debt
    df.loc[:, "Amount / Total Debt"] = df.apply(lambda row: row["Amount"] / max(row["Total Debt"], 1), axis=1)

    # 4. user City == merchant city
    df.loc[:, "user City = merchant city"] = df.apply(lambda row: 1 if row["Merchant City"] == row["City"] else 0, axis=1)
    df = df.drop(["City", "Merchant City"], axis=1)
    return df