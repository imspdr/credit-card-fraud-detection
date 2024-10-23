import pandas as pd


df = pd.read_csv("../data/processed/eval_data.csv")

df[-10:].to_json("jsoneval.json", orient="records")