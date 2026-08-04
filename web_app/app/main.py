from sqlmodel import select, Session

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from web_app.app.database import create_db_and_tables, get_session
from web_app.app.models import Measurement

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Stacja pogodowa działa!"}


@app.post("/api/v1/measurements", response_model=Measurement)
def add_measurement(
    measurement: Measurement,
    session: Session = Depends(get_session),
):
    session.add(measurement)
    session.commit()
    session.refresh(measurement)
    return measurement


@app.get("/api/v1/measurements", response_model=list[Measurement])
async def get_measurements(
    session: Session = Depends(get_session),
):
    measurements = session.exec(select(Measurement)).all()
    return measurements
