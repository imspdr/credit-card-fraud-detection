from fastapi import FastAPI, HTTPException, Depends
import httpx
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models import *
from db import *
from contextlib import asynccontextmanager
import logging
import json
import pandas as pd
import numpy as np
import pickle

from model.feature_engineering.preprocess_user_card import preprocess_user, preprocess_card
from model.feature_engineering.generate_user_feature import generate_user_feature
from model.feature_engineering.preprocessing import preprocessing
from model.feature_engineering.generate_age_feature import generate_age_feature
from model.feature_engineering.add_fraud_one_hot import add_fraud_one_hot
import pytz
import os


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

kst = pytz.timezone('Asia/Seoul')

Base.metadata.create_all(bind=engine)

user_mapper = {}
card_mapper = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("add card, user csv to db")
    load_user_to_db()
    load_card_to_db()

    yield

    print("shutting down server. drop user, card table")
    User.__table__.drop(engine)
    Card.__table__.drop(engine)

app = FastAPI(lifespan=lifespan)

ISTIO_IP = os.getenv("ISTIO_IP", "192.168.49.2")
ISTIO_PORT = os.getenv("ISTIO_PORT", "31397")
NAMESPACE = os.getenv("NAMESPACE", "default")
EXTERNAL_URL = f"http://{ISTIO_IP}:{ISTIO_PORT}/v1/models/fraud-detection-serving:predict"
HEADERS = {
    "Host": f"fraud-detection-serving.{NAMESPACE}.example.com",
    "Content-Type": "application/json",
}
TRANSACTION_KEYS = ["User", "Card", "Time", "Amount", "Use Chip", "Merchant Name", "Merchant City", "Merchant State","Zip", "MCC"]

with open("ensemble_model.pkl", "rb") as pkl_file:
    models = pickle.load(pkl_file)

@app.post("/inference")
async def inference_api(request_data: List[Dict[str, Any]], db: Session = Depends(get_db)):
    try:
        user_info_list = []
        card_info_list = []
        user_cache = []
        card_cache = []
        for item in request_data:
            # STEP1. validation
            for key in TRANSACTION_KEYS:
                try:
                    item[key]
                except KeyError:
                    raise Exception("input data invalid")
            # STEP2. load user, card info from db
            user_id = item["User"]
            card_id = item["Card"]
            user_info, card_info = fetch_data_from_db(db, user_id, card_id)
            if not user_id in user_cache:
                user_info_list.append(user_info)
                user_cache.append(user_id)
            if not (user_id, card_id) in card_cache:
                card_info_list.append(card_info)
                card_cache.append((user_id, card_id))

        # STEP3. send request to inference service of kserve
        payload = {
            "instances": [],
            "user": user_info_list,
            "card": card_info_list,
            "transaction": request_data
        }

        logging.info("[predictor] start serving")
        df = pd.DataFrame(payload["transaction"])
        user_df = preprocess_user(pd.DataFrame(payload["user"]))
        card_df = preprocess_card(pd.DataFrame(payload["card"]))

        logging.info(f"[predictor] successfully read request data length : {len(df)}")
        df = preprocessing(df, card_df, user_df)
        df = generate_age_feature(df)
        df = add_fraud_one_hot(df)
        df = generate_user_feature(df)

        logging.info("[predictor] successfully done feature engineering")
        result = []

        logging.info("[predictor] start prediction")
        for i, model in enumerate(models):
            y_hat = model.inference_proba(df.to_numpy())
            result.append(y_hat)

        logging.info("[predictor] prediction done")
        y_hats_array = np.array(result)
        mean_y_hat = np.mean(y_hats_array, axis=0)

        result = {
            "predictions": mean_y_hat,
        }
        json_result = json.dumps(obj=result, cls=NpEncoder, indent=4, ensure_ascii=False)
        return json.loads(json_result)

    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

def fetch_data_from_db(db: Session, user_id: int, card_id: int):
    selected_user = db.query(User).filter(User.id == user_id).first()
    selected_card = db.query(Card).filter(Card.user == user_id, Card.card_index == card_id).first()

    if not selected_user or not selected_card:
        raise HTTPException(status_code=404, detail="User or Card not found")

    selected_user = vars(selected_user)
    selected_card = vars(selected_card)
    user_info = {}
    for key, value in user_mapper.items():
        user_info[value] = selected_user[key]

    card_info = {}
    for key, value in card_mapper.items():
        card_info[value] = selected_card[key]

    return user_info, card_info

def load_user_to_db():
    global user_mapper
    session = SessionLocal()
    try:
        df = pd.read_csv("sd254_users_with_id.csv")
        old_columns = df.columns
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('-', '1').str.lower()

        for i, col in enumerate(old_columns):
            user_mapper[df.columns[i]] = col

        for i, row in df.iterrows():
            if pd.isna(row["apartment"]):
                row["apartment"] = "no"
            user = User(**row.to_dict())
            session.add(user)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error loading user csv: {e}")
    finally:
        session.close()

def load_card_to_db():
    global card_mapper
    session = SessionLocal()
    try:
        df = pd.read_csv("sd254_cards.csv")
        old_columns = df.columns
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
        for i, col in enumerate(old_columns):
            card_mapper[df.columns[i]] = col
        for _, row in df.iterrows():
            card = Card(**row.to_dict())
            session.add(card)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error loading card csv: {e}")
    finally:
        session.close()