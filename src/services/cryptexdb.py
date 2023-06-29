import os
from datetime import date

from peewee import *

from apiresponses import LeaderboardEntry, PlayerStatistics, PlayerInfo
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

        CryptexDB.psql_db.create_tables([Player, PlayerStats, ActivePuzzle])

    @staticmethod
    def register_player(player_id: str, name: str):
        player = Player.create(id=player_id, name=name)
        PlayerStats.create(player_id=player)
        ActivePuzzle.create(player_id=player)

    @staticmethod
    def player_started_new_game(player_id: str, new_solution: str, points: int):
        ActivePuzzle.update(solution=new_solution, points=points, tries=3).where(
            ActivePuzzle.player_id == player_id).execute()

        PlayerStats.update(games_played=PlayerStats.games_played + 1).where(
            PlayerStats.player_id == player_id).execute()

    @staticmethod
    def get_player_active_puzzle(player_id: str) -> PlayerActivePuzzle:
        puzzle = ActivePuzzle.get(ActivePuzzle.player_id == player_id)
        return PlayerActivePuzzle(Solution=puzzle.solution, Points=puzzle.points, Tries=puzzle.tries)

    @staticmethod
    def player_won(player_id: str, points: int):
        ActivePuzzle.update(solution=None, points=0, tries=0).where(ActivePuzzle.player_id == player_id).execute()
        PlayerStats.update(games_won=PlayerStats.games_won + 1, score=PlayerStats.score + points).where(
            PlayerStats.player_id == player_id).execute()

    @staticmethod
    def player_tries_again(player_id: str):
        ActivePuzzle.update(tries=ActivePuzzle.tries - 1).where(ActivePuzzle.player_id == player_id).execute()

    @staticmethod
    def player_lost(player_id: str):
        ActivePuzzle.update(solution=None, points=0, tries=0).where(ActivePuzzle.player_id == player_id).execute()

    @staticmethod
    def get_all_players_info() -> dict[str, PlayerInfo]:
        info = Player.select(Player.id, Player.name, Player.joined_date)
        return {x.id: PlayerInfo(Name=x.name, DateJoined=x.joined_date) for x in info}

    @staticmethod
    def get_player_info(player_id: str) -> PlayerInfo:
        info = Player.get(Player.id == player_id)
        return PlayerInfo(Name=info.name, DateJoined=info.joined_date)

    @staticmethod
    def get_all_players_stats() -> dict[str, PlayerStatistics]:
        stats = PlayerStats.select(PlayerStats.player_id, PlayerStats.games_played, PlayerStats.games_won,
                                   PlayerStats.score).namedtuples()

        return {x.player_id: PlayerStatistics(GamesPlayed=x.games_played, GamesWon=x.games_won, Score=x.score) for x
                in stats}

    @staticmethod
    def get_player_stats(player_id: str) -> PlayerStatistics:
        stats = Player.get(Player.id == player_id).stats.get()
        return PlayerStatistics(GamesPlayed=stats.games_played, GamesWon=stats.games_won,
                                Score=stats.score)

    @staticmethod
    def get_leaderboard() -> dict[str, LeaderboardEntry]:
        leaderboard = Player.select(Player.id, Player.name, PlayerStats.score).join(PlayerStats).order_by(
            PlayerStats.score.desc()).namedtuples()
        return {x.id: LeaderboardEntry(Name=x.name, Score=x.score) for x in leaderboard}

    @staticmethod
    def delete_player(player_id: str):
        Player.delete().where(Player.id == player_id).execute()


class BaseModel(Model):
    class Meta:
        database = CryptexDB.psql_db


class Player(BaseModel):
    id = CharField(36, primary_key=True)
    name = CharField(50, unique=True)
    joined_date = DateField(default=date.today())


class ActivePuzzle(BaseModel):
    player_id = ForeignKeyField(Player, index=True, primary_key=True, backref='active_puzzle', on_delete='CASCADE')
    solution = CharField(15, null=True)
    points = SmallIntegerField(default=0)
    tries = SmallIntegerField(default=0)


class PlayerStats(BaseModel):
    player_id = ForeignKeyField(Player, index=True, primary_key=True, backref='stats', on_delete='CASCADE')
    games_played = IntegerField(default=0)
    games_won = IntegerField(default=0)
    score = IntegerField(default=0)
