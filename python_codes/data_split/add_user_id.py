import pandas as pd

user_df = pd.read_csv("../data/given/sd254_users.csv")
user_df.reset_index(inplace=True)
user_df.rename(columns={"index": "id"}, inplace=True)
user_df.to_csv("../data/processed/sd254_users_with_id.csv", index=False)
