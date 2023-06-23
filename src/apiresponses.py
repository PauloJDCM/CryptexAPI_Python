from datetime import date
from pydantic import BaseModel


class Puzzle(BaseModel):
    class Config:
        allow_mutation = False

    Puzzle: list[list[str]]
    Descriptions: list[str]
    Points: int


class CheckResult(BaseModel):
    class Config:
        allow_mutation = False

    IsCorrect: bool
    TriesLeft: int


class LeaderboardEntry(BaseModel):
    class Config:
        allow_mutation = False

    PlayerName: str
    Score: int


class Leaderboard(BaseModel):
    class Config:
        allow_mutation = False

    Entries: list[LeaderboardEntry] = []


class PlayerStatistics(BaseModel):
    class Config:
        allow_mutation = False

    Id: str
    GamesPlayed: int
    GamesWon: int
    Score: int


class PlayerInfo(BaseModel):
    class Config:
        allow_mutation = False

    Id: str
    Name: str
    DateJoined: date
