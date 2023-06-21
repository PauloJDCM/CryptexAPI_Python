import json
import os
import random
import string
from pydantic import BaseModel

from apiresponses import Puzzle
from data.cryptexdtos import GeneratedPuzzle, Difficulty, DifficultyOptions


class Word(BaseModel):
    class Config:
        allow_mutation = False

    Value: str
    Key: str


class PuzzleSequence(BaseModel):
    class Config:
        allow_mutation = False

    Value: list[list[str]] = []


class PuzzleGenerator:
    def __init__(self):
        self.AllowedCharacters: str = string.ascii_uppercase
        self.BasePoints: int = int(os.getenv('BASE_POINTS'))

        with open('./data/CryptexDict_Words.json') as file:
            self.Words: dict[str, list[list[str]]] = json.load(file)

        with open('./data/CryptexDict_Descriptions.json') as file:
            self.Descriptions: dict[str, list[str]] = json.load(file)

    def generate(self, difficulty: int) -> GeneratedPuzzle:
        options = Difficulty(difficulty).get_options()

        word = self._get_random_word(options)
        description = self.Descriptions[word.Key]
        points = self._calculate_points(options, word)
        puzzle_sequence = self._generate_puzzle_sequence(word.Value, options)

        puzzle = Puzzle(Puzzle=puzzle_sequence.Value, Descriptions=description, Points=points)
        return GeneratedPuzzle(Puzzle=puzzle, Solution=word.Value)

    def _get_random_word(self, options: DifficultyOptions) -> Word:
        length = str(random.sample(options.ComplexityRange, 1)[0])
        word = random.sample(self.Words[length], 1)[0]

        return Word(Value=word[0], Key=word[1])

    def _calculate_points(self, options: DifficultyOptions, word: Word) -> int:
        return options.ScoreMultiplier * len(word.Value) * self.BasePoints

    def _generate_puzzle_sequence(self, word: str, options: DifficultyOptions) -> PuzzleSequence:
        puzzle = PuzzleSequence()

        for char in word:
            seen_characters = [char]

            for i in range(options.Permutations + 1):
                new_char = char
                while new_char in seen_characters:
                    new_char = random.sample(self.AllowedCharacters, 1)[0]

                seen_characters.append(new_char)

            random.shuffle(seen_characters)
            puzzle.Value.append(seen_characters)

        return puzzle
