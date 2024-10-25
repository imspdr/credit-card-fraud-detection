import pandas as pd

def add_fraud_one_hot(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Use Chip - one hot encoding
    df.loc[:, "Use Chip = Online"] = df["Use Chip"].apply(lambda chip: 1 if chip == "Online Transaction" else 0)
    df.loc[:, "Use Chip = Swipe"] = df["Use Chip"].apply(lambda chip: 1 if chip == "Swipe Transaction" else 0)
    df = df.drop(["Use Chip"], axis=1)

    # 2. Merchant State - Italy one hot encoding
    df.loc[:, "Merchant State = Italy"] = df["Merchant State"].apply(lambda state: 1 if state == "Italy" else 0)
    df = df.drop(["Merchant State"], axis=1)

    # 3. Zip - 44680  one hot encoding
    df.loc[:, "Zip = 44680"] = df["Zip"].apply(lambda zip: 1 if zip == 44680.0 else 0)
    df = df.drop(["Zip"], axis=1)

    # 4. MCC - 5311 one hot encoding
    df.loc[:, "MCC = 5311"] = df["MCC"].apply(lambda state: 1 if state == 5311 else 0)
    df = df.drop(["MCC"], axis=1)
    return df