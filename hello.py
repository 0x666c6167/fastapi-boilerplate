from enum import Enum
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Run the app with `uvicorn hello:app --reload`
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Host(BaseModel):
    hostname: str
    ipv4_addr: Optional[str] = None
    username: str
    password: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/params/") 
async def query_params(foo: int = 0, bar: int = 42, baz: Optional[str] = None):
    if baz:
        return {"foo": foo, "bar": bar, "baz": baz}
    else:
        return {"foo": foo, "bar": bar}

# Need a request body - use pydantic BaseModel
@app.post("/hosts/")
async def create_host(host: Host):
    return host