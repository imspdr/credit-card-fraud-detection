import pandas as pd

def add_fraud_one_hot(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Use Chip - one hot encoding
    df.loc[:, "Use Chip = Online"] = df["Use Chip"].apply(lambda chip: 1 if chip == "Online Transaction" else 0)
    df.loc[:, "Use Chip = Swipe"] = df["Use Chip"].apply(lambda chip: 1 if chip == "Swipe Transaction" else 0)
    df = df.drop(["Use Chip"], axis=1)

    # 2. Merchant State - Italy one hot encoding
    df.loc[:, "Merchant State = Italy"] = df["Merchant State"].apply(lambda state: 1 if state == "Italy" else 0)
    df = df.drop(["Merchant State"], axis=1)
    return df