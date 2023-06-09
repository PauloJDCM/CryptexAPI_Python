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

    Name: str
    Score: int


class PlayerStatistics(BaseModel):
    class Config:
        allow_mutation = False

    GamesPlayed: int
    GamesWon: int
    Score: int


class PlayerInfo(BaseModel):
    class Config:
        allow_mutation = False

    Name: str
    DateJoined: date
