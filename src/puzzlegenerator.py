from data.cryptexdtos import Puzzle, DifficultyOptions


class CryptexGenerator:

    def generate_puzzle(self, options: DifficultyOptions) -> Puzzle:
        return Puzzle(Solution='', Descriptions=[], Puzzle=[])
