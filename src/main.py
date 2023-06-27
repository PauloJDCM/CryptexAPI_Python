from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from peewee import IntegrityError, DoesNotExist

from apiresponses import *
from services.cryptexdb import CryptexDB
from services.puzzlegenerator import PuzzleGenerator

load_dotenv("cryptexapi.env")

app = FastAPI()
db = CryptexDB()
puzzle_gen = PuzzleGenerator()


@app.post("/players/{external_id}")
async def register_player(external_id: str, name: str):
    try:
        db.register_player(external_id=external_id, name=name)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="ID or name already in use")


@app.get("/players", response_model=dict[str, PlayerInfo])
async def get_all_players_info():
    return db.get_all_players_info()


@app.get("/players/{external_id}", response_model=PlayerInfo)
async def get_player_info(external_id: str):
    try:
        return db.get_player_info(external_id)
    except DoesNotExist:
        raise HTTPException(status_code=404)


# fastapi not accepting non-trailing slash path
@app.get("/players/stats/", response_model=dict[str, PlayerStatistics])
async def get_all_players_stats():
    return db.get_all_players_stats()


@app.get("/players/stats/{external_id}", response_model=PlayerStatistics)
async def get_player_stats(external_id: str):
    try:
        return db.get_player_stats(external_id)
    except DoesNotExist:
        raise HTTPException(status_code=404)


@app.get("/puzzles/{external_id}", response_model=Puzzle)
async def generate_puzzle(external_id: str, difficulty: int):
    try:
        generated = puzzle_gen.generate(difficulty)

        db.player_started_new_game(external_id=external_id, new_solution=generated.Solution,
                                   points=generated.Puzzle.Points)

        return generated.Puzzle
    except DoesNotExist:
        raise HTTPException(status_code=404)
    except ValueError:
        raise HTTPException(status_code=400, detail="Difficulty not valid! Only digits from 1 to 3 are allowed")


@app.put("/puzzles/{external_id}", response_model=CheckResult)
async def check_solution(external_id: str, solution: str):
    try:
        active_puzzle = db.get_player_active_puzzle(external_id)
    except DoesNotExist:
        raise HTTPException(status_code=404)

    if active_puzzle.Solution is None:
        raise HTTPException(status_code=400, detail="Player has no active puzzles")

    active_puzzle.Tries -= 1

    if active_puzzle.Solution == solution.upper():
        db.player_won(active_puzzle.PlayerId, active_puzzle.Points)
        return CheckResult(IsCorrect=True, TriesLeft=active_puzzle.Tries)

    if active_puzzle.Tries > 0:
        db.player_tries_again(active_puzzle.PlayerId)
        return CheckResult(IsCorrect=False, TriesLeft=active_puzzle.Tries)

    db.player_lost(active_puzzle.PlayerId)
    return CheckResult(IsCorrect=False, TriesLeft=active_puzzle.Tries)


@app.get("/leaderboard", response_model=dict[str, LeaderboardEntry])
async def get_leaderboard():
    return db.get_leaderboard()


@app.delete("/players/{external_id}")
async def remove_player(external_id: str):
    db.delete_player(external_id)
