from dotenv import load_dotenv
from fastapi import FastAPI
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
