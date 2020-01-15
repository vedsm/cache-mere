from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response, JSONResponse

import logging
import json


from src.event_receiving.event_publisher import EventPublisher

app = FastAPI()
log = logging.getLogger("app")
event_publisher = EventPublisher()

@app.get("/")
def read_root():
    return {"version": "0.1","name":"Cache-Mere event receiver REST API"}


@app.route("/health")
def health():
    return {"status": "ok"}

from pydantic import BaseModel
class BodyData(BaseModel):
    msg: dict # = {"lat":17.385044, "lon": 78.486671, "malaria": 1, "violence": 0, "litchi": 0}

@app.post("/v1/event/receive")
def event_published(
    body_data: BodyData
    ):
    # return {"status": "ok", "msg": msg}
    msg = body_data.msg
    if msg:
        log.info("An event is received on REST API: {}".format(msg))
        publishing_response = event_publisher.publish(msg)

        return JSONResponse(
            status_code=200,
            content=publishing_response,
        )
    else:
        # log.error("ERROR: {}".format(e))
        log.error("No msg found in the request body")
        return JSONResponse(
            status_code=422,
        )

