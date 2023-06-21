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


class PlayerStanding(BaseModel):
    class Config:
        allow_mutation = False

    Score: int
    FocusedLeaderboard: Leaderboard


class PlayerStats(BaseModel):
    class Config:
        allow_mutation = False

    GamesPlayed: int
    GamesWon: int
    Score: int
