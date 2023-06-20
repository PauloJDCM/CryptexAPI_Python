from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from services.cryptexdb import CryptexDB
from apiresponses import *

load_dotenv("cryptexapi.env")

app = FastAPI()
db = CryptexDB()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/players/{external_id}")
async def register_player(external_id: str, name: str):
    db.register_player(external_id=external_id, name=name)


@app.get("/puzzles/{external_id}", response_model=Puzzle)
async def generate_puzzle(external_id: str, difficulty: int):
    test_puzzle = Puzzle(Puzzle=[], Descriptions=[])

    db.player_started_new_game(external_id=external_id, new_solution="TEST", points=100)
    return test_puzzle


@app.put("/puzzles/{external_id}", response_model=CheckResult)
async def check_solution(external_id: str, solution: str):
    active_puzzle = db.get_player_active_puzzle(external_id)

    if active_puzzle.Solution is None:
        raise HTTPException(status_code=400, detail="Player has no active puzzles")

    active_puzzle.Tries -= 1

    if active_puzzle.Solution == solution:
        db.player_won(active_puzzle.PlayerId, active_puzzle.Points)
        return CheckResult(IsCorrect=True, TriesLeft=active_puzzle.Tries)

    if active_puzzle.Tries > 0:
        db.player_tries_again(active_puzzle.PlayerId)
        return CheckResult(IsCorrect=False, TriesLeft=active_puzzle.Tries)

    db.player_lost(active_puzzle.PlayerId)
    return CheckResult(IsCorrect=False, TriesLeft=active_puzzle.Tries)
