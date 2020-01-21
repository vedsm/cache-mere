from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response, JSONResponse
from pydantic import BaseModel


import logging
import json


app = FastAPI()
log = logging.getLogger("app")

@app.get("/")
def read_root():
    return {"version": "0.1","name":"Find what you lost REST API"}


@app.route("/health")
def health():
    return {"status": "ok"}

class BodyData(BaseModel):
    since_when: str
    lat: float
    lon: float
    tags: list
    # msg: dict # = {"lat":17.385044, "lon": 78.486671, "malaria": 1, "violence": 0, "litchi": 0}

@app.post("/v1/please_find_it")
def please_find_it(
    body_data: BodyData
    ):
    log.info("An event is received on REST API: {}".format(body_data))

    return JSONResponse(
        status_code=200,
        # content=body_data,
    )

