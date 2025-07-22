"""FastAPI microservice for inspecting incoming JSON payloads."""

from typing import Dict, Any
import os
from fastapi import FastAPI, Header, Depends, HTTPException, Body
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


def verify_api_key(x_api_key: str = Header(...)):
    """Check for api key passed in headers"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")


@app.get("/health", tags=["utility"])
async def get_health():
    """health check"""
    return {"status": "ok"}


@app.post("/inspect", tags=["utility"])
async def inspect(data: Dict[str, Any], _: None = Depends(verify_api_key)):
    """Parse the request body"""
    null_count = 0
    nested_count = 0
    key_types = {}

    for key, value in data.items():
        key_types[key] = type(value).__name__
        if value is None:
            null_count += 1
        elif isinstance(value, dict):
            nested_count += 1

    return {
        "type": type(data).__name__,
        "length": len(data),
        "keys": list(data.keys()),
        "value_type": key_types,
        "null_values": null_count,
        "nested_objects": nested_count,
    }


@app.post("/transform", tags=["utility"])
async def transform(
    data: Dict[str, Any] = Body(...), _: None = Depends(verify_api_key)
):
    """Remove any null values from inbound payload"""
    cleaned = {k: v for k, v in data.items() if v is not None}
    return cleaned
