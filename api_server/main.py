from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from api_server.schemas import *
from api_server.db import *
from infra.k8s_operations import *
from kubernetes import config
from kubernetes.config.config_exception import ConfigException
import pytz

kst = pytz.timezone('Asia/Seoul')

Base.metadata.create_all(bind=engine)

try:
    config.load_incluster_config()
except ConfigException as e:
    print(f"Failed to load kube-config: {e}")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/inference/")
async def create_train_api(train_create: TrainCreate, db: Session = Depends(get_db)):

    return

@app.get("/sample/")
def get_train_all_api(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return
