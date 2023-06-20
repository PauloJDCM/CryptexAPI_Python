from pydantic import BaseModel


class Puzzle(BaseModel):
    Puzzle: list[str]
    Descriptions: list[str]


class CheckResult(BaseModel):
    IsCorrect: bool
    TriesLeft: int


class LeaderboardEntry(BaseModel):
    PlayerName: str
    Score: int


class Leaderboard(BaseModel):
    Entries: list[LeaderboardEntry] = []


class PlayerStanding(BaseModel):
    Score: int
    FocusedLeaderboard: Leaderboard


class PlayerStats(BaseModel):
    GamesPlayed: int
    GamesWon: int
    Score: int
