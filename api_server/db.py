from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

MYSQL_IP = os.getenv("MYSQL_IP", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "30007")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DB = os.getenv("MYSQL_DB", "rain")

DB_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_IP}:{MYSQL_PORT}/{MYSQL_DB}"
#DB_URL = "mysql+pymysql://root:root@192.168.49.2:30007/rain"
#DB_URL = "mysql+pymysql://root:root@192.168.99.100:30007/rain"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
