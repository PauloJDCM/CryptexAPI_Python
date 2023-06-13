from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()
load_dotenv("../cryptexapi.env")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
