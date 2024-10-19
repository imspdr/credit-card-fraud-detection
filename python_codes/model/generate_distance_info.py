import pandas as pd
import numpy as np
import requests
from tqdm import tqdm

cache = {}
tqdm.pandas()

def get_latitude_longitude_from_zip(zip_code, country="us"):
    global cache
    if zip_code in cache.keys():
        return cache[zip_code]

    url = f"https://api.zippopotam.us/{country}/{zip_code}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        place = data["places"][0]
        cache[zip_code] = (float(place["latitude"]), float(place["longitude"]))
        return float(place["latitude"]), float(place["longitude"])
    else:
        return None, None

def calculate_distance(transaction_zip, user_latitude, user_longitude):
    if not transaction_zip or np.isnan(transaction_zip):
        return 0

    # get latitude and longitude info from transaction zip code
    transaction_latitude, transaction_longitude = get_latitude_longitude_from_zip(int(transaction_zip))

    if not (transaction_longitude and transaction_latitude):
        return 0
    # calculate the gap of values (distance doesn't need to be actual distance
    return abs(transaction_latitude - user_latitude) + abs(transaction_longitude - user_longitude)

def generate_distance_info(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[:, "distance"] = df.progress_apply(lambda row: calculate_distance(row["Zip"], row["Latitude"], row["Longitude"]), axis=1)
    return df

