from sqlalchemy import Column, Integer, String, DateTime, Text, LargeBinary, ForeignKey
from sqlalchemy.sql import func

from .db import Base


class RainTrain(Base):
    __tablename__ = 'rain_trains'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    cpu_size = Column(String(50), nullable=False, default="1000m")
    memory_size = Column(String(50), nullable=False, default="1Gi")
    start_day = Column(String(50), nullable=False)
    end_day = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    finished_at = Column(DateTime, nullable=True, default=None)

    status = Column(String(255), nullable=False, default="creating")

    def __repr__(self):
        return f"<Train(id={self.id}, name={self.name}, created_at={self.created_at})>"

class RainTrainedModel(Base):
    __tablename__ = 'rain_trained_models'
    id = Column(Integer, primary_key=True, autoincrement=True)
    train_name = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    data_distribution = Column(Text, nullable=False)
    trained_model_info = Column(Text, nullable=False)
    trained_model_pkl = Column(LargeBinary(length=(2**32)-1), nullable=True)
    deployed = Column(String(50), nullable=False, default="false")

    def __repr__(self):
        return f"<TrainedModel(id={self.id}, name={self.name})>"
