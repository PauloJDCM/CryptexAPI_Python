import os
from datetime import date
from peewee import *

from data.cryptexdtos import PlayerActivePuzzle


class CryptexDB:
    psql_db: PostgresqlDatabase = PostgresqlDatabase(None)

    def __init__(self):
        CryptexDB.psql_db.init(
            database='postgres',
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('DB_HOSTNAME'),
            port=os.getenv('DB_HOSTPORT')
        )

        CryptexDB.psql_db.create_tables([Player, PlayerStats])

    @staticmethod
    def register_player(external_id: str, name: str):
        player = Player(external_id=external_id, name=name)
        player.save()

        PlayerStats(player_id=player.id).save()
        ActivePuzzle(player_id=player.id).save()

    @staticmethod
    def player_started_new_game(external_id: str, new_solution: str, points: int):
        player_id = CryptexDB._get_player_id(external_id)

        puzzles_update = ActivePuzzle.update(solution=new_solution, points=points)
        stats_update = PlayerStats.update(games_played=PlayerStats.games_played + 1).where(
            PlayerStats.player_id == player_id)

        puzzles_update.execute()
        stats_update.execute()

    @staticmethod
    def get_player_active_puzzle(external_id: str) -> PlayerActivePuzzle:
        player_id = CryptexDB._get_player_id(external_id)
        puzzle = ActivePuzzle.get(ActivePuzzle.player_id == player_id)

        return PlayerActivePuzzle(PlayerId=player_id, Solution=puzzle.solution, Points=puzzle.points,
                                  Tries=puzzle.tries)

    @staticmethod
    def player_won(player_id: int, points: int) -> int:
        ActivePuzzle.update(solution=None, points=0, tries=0).where(Player.id == player_id).execute()
        PlayerStats.update(games_won=PlayerStats.games_won + 1, score=PlayerStats.score + points).where(
            PlayerStats.player_id == player_id).execute()

        return PlayerStats.get(PlayerStats.player_id == player_id).score

    @staticmethod
    def player_tries_again(player_id: int):
        ActivePuzzle.update(tries=ActivePuzzle.tries - 1).where(ActivePuzzle.player_id == player_id).execute()

    @staticmethod
    def player_lost(player_id: int):
        ActivePuzzle.update(solution=None, points=0, tries=0).where(ActivePuzzle.player_id == player_id).execute()

    @staticmethod
    def _get_player_id(external_id: str) -> int:
        return Player.get(Player.external_id == external_id).id


class BaseModel(Model):
    class Meta:
        database = CryptexDB.psql_db


class Player(BaseModel):
    id = IdentityField()
    external_id = CharField(36, index=True)
    name = CharField(50)
    joined_date = DateField(default=date.today())


class ActivePuzzle(BaseModel):
    id = IdentityField()
    player_id = ForeignKeyField(Player, backref='active_puzzle')
    solution = CharField(15, null=True)
    points = SmallIntegerField(default=0)
    tries = SmallIntegerField(default=0)


class PlayerStats(BaseModel):
    id = IdentityField()
    player_id = ForeignKeyField(Player, backref='stats')
    games_played = IntegerField(default=0)
    games_won = IntegerField(default=0)
    score = IntegerField(default=0)
