from dotenv import load_dotenv
from fastapi import FastAPI

from data.cryptexdtos import Puzzle
from services.cryptexdb import CryptexDB

load_dotenv("cryptexapi.env")

app = FastAPI()
db = CryptexDB()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/players")
async def register_player(externalid: str, name: str):
    db.register_player(external_id=externalid, name=name)
