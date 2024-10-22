from pydantic import BaseModel

class TrainCreate(BaseModel):
    name: str
    cpu_size: str
    memory_size: str
    start_day: str
    end_day: str
    class Config:
        from_attributes = True

class TrainedModel(BaseModel):
    train_name: str
    name: str
    data_distribution: str
    trained_model_info: str
    class Config:
        from_attributes = True

class Train(TrainCreate):
    id: int
    created_at: str
    finished_at: str | None
    status: str
    class Config:
        from_attributes = True
