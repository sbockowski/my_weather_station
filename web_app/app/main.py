from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Measurement


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index_view(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/partials/measurement", response_class=HTMLResponse)
def partial_measurements_view(
    request: Request,
    session: Session = Depends(get_session),
):
    statement = select(Measurement).order_by(Measurement.id.desc()).limit(1)
    latest_measurement = session.exec(statement).first()

    return templates.TemplateResponse(
        request=request,
        name="partials/table.html",
        context={"measurement": latest_measurement},
    )


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
