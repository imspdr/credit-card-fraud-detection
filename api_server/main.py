from fastapi import FastAPI, HTTPException, Request
import httpx
from sqlalchemy.orm import Session
from models import *
from db import *
from contextlib import asynccontextmanager
import pytz
import os
import pandas as pd

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
EXTERNAL_URL = f"http://{ISTIO_IP}:{ISTIO_PORT}/v1/models/fraud-detection-serving:predict"
HEADERS = {
    "Host": "fraud-detection-serving.default.example.com",
    "Content-Type": "application/json",
}
@app.post("/inference/")
async def inference_api(request: Request):

    try:
        request_data = await request.json()

        async with httpx.AsyncClient() as client:
            response = await client.post(EXTERNAL_URL, json=request_data, headers=HEADERS)

        response.raise_for_status()

        return response.json()

    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


def load_user_to_db():
    global user_mapper
    session = SessionLocal()
    try:
        df = pd.read_csv("./sd254_users_with_id.csv")
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
        df = pd.read_csv("./sd254_cards.csv")
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