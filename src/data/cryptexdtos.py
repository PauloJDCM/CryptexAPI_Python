from pydantic import BaseModel
from enum import IntEnum


class DifficultyOptions(BaseModel):
    class Config:
        allow_mutation = False

    ComplexityRange: range
    Permutations: int
    ScoreMultiplier: int


class Puzzle(BaseModel):
    Descriptions: list[str]
    Puzzle: list[str]


class Difficulty(IntEnum):
    Easy = 1
    Medium = 2
    Hard = 3

    def get_options(self) -> DifficultyOptions:
        match self:
            case Difficulty.Easy:
                return DifficultyOptions(ComplexityRange=range(4, 7), Permutations=4, ScoreMultiplier=1)

            case Difficulty.Medium:
                return DifficultyOptions(ComplexityRange=range(3, 10), Permutations=6, ScoreMultiplier=4)

            case Difficulty.Hard:
                return DifficultyOptions(ComplexityRange=range(0, 100), Permutations=8, ScoreMultiplier=9)