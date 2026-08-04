from sqlmodel import Field, SQLModel
import datetime as dt

class Measurement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    temperature: float
    humidity: float
    pressure: float
    timestamp: dt.datetime = Field(default_factory=dt.datetime.now)