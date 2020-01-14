from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response, JSONResponse

import logging
import json

app = FastAPI()
log = logging.getLogger("app")

@app.get("/")
def read_root():
    return {"version": "0.1","name":"Cache-Mere event consumer REST API"}


@app.route("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/events/publish")
def event_published(data):
    # return {"status": "ok", "data": data}
    # log.error("ERROR: {}".format(e))
    log.info("An event is published: {}".format(data))

    return JSONResponse(
        status_code=200,
        content=data,
    )
