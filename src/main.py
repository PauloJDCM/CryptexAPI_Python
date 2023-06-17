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


@app.post("/players/{id}")
async def register_player(id: str, name: str):
    db.register_player(external_id=id, name=name)


@app.get("/puzzles/{player_id}/{difficulty}", response_model=Puzzle)
async def generate_puzzle(player_id: str, difficulty: int):
    test_puzzle = Puzzle(Puzzle=[], Descriptions=[])

    db.player_started_new_game(external_id=player_id, new_solution="TEST", points=100)
    return test_puzzle.json()


@app.put("/puzzles/{player_id}/")
async def check_solution(player_id: str, solution: str):
    active_puzzle = db.get_player_active_puzzle(player_id)
    active_puzzle.Tries -= 1

    if active_puzzle.Solution == solution:
        db.player_won(active_puzzle.PlayerId, active_puzzle.Points)
    elif active_puzzle.Tries > 0:
        db.player_tries_again(active_puzzle.PlayerId)
    else:
        db.player_lost(active_puzzle.PlayerId)

