from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from src.prediction import ModelUnavailable
from src.model_manager import ModelManager
from src.training import DEFAULT_MODEL

Move = Literal["ROCK", "PAPER", "SCISSORS"]
logger = logging.getLogger(__name__)


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    history: list[Move] = Field(min_length=3, max_length=3)


class PredictionResponse(BaseModel):
    predictedMove: Move
    confidence: float = Field(ge=0, le=1)
    probabilities: dict[Move, float]
    modelName: str
    modelVersion: str
    historyLength: int


def create_app(model_path=None):
    path = Path(model_path or os.environ.get("MODEL_PATH", DEFAULT_MODEL))

    @asynccontextmanager
    async def lifespan(application):
        application.state.models = ModelManager(path)
        application.state.models.get()
        yield

    application = FastAPI(title="Jack-En-Poy prediction service", version="1.0.0", lifespan=lifespan)

    @application.get("/health")
    def health():
        predictor = application.state.models.get()
        if predictor is None:
            return JSONResponse(status_code=503, content={"status": "unavailable", "modelLoaded": False})
        return {"status": "ready", "modelLoaded": True, "reloadFailed": application.state.models.reload_failed, "modelName": predictor.artifact["modelName"], "modelVersion": predictor.artifact["modelVersion"]}

    @application.post("/predict", response_model=PredictionResponse)
    def predict(request: PredictionRequest):
        predictor = application.state.models.get()
        if predictor is None:
            raise HTTPException(status_code=503, detail="Prediction model unavailable")
        try:
            return predictor.predict(request.history)
        except ModelUnavailable as error:
            raise HTTPException(status_code=503, detail="Prediction model unavailable") from error

    return application


app = create_app()
