from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response, JSONResponse

import logging
import json

from src.event_broker.event_broker_publisher import EventBrokerPublisher

app = FastAPI()
log = logging.getLogger("app")
event_broker_publisher = EventBrokerPublisher()

@app.get("/")
def read_root():
    return {"version": "0.1","name":"Cache-Mere event receiver REST API"}


@app.route("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/event/receive")
def event_published(msg):
    # return {"status": "ok", "msg": msg}
    # log.error("ERROR: {}".format(e))
    log.info("An event is received on REST API: {}".format(msg))
    event_broker_publisher.publish(msg)

    return JSONResponse(
        status_code=200,
        content=msg,
    )
