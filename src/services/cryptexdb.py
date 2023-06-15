import os
from sqlalchemy import create_engine, insert, update, select
from data.cryptexmodels import Base, Player, PlayerStats


class CryptexDB:
    def __init__(self):
        self._engine = create_engine(
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@db:5432/postgres", echo=True)
        Base.metadata.create_all(self._engine)

    def register_player(self, external_id: str, name: str):
        with self._engine.connect() as conn:
            stmt = (
                insert(Player)
                .values(external_id=external_id, name=name)
            )
            new_player_id = conn.execute(stmt).inserted_primary_key[0]

            stmt = (
                insert(PlayerStats)
                .values(player_id=new_player_id, games_played=0, games_won=0, score=0)
            )
            conn.execute(stmt)

            conn.commit()

    def player_won(self, player_id: int, points: int) -> int:
        with self._engine.connect() as conn:
            stats = conn.execute(
                select(PlayerStats)
                .where(PlayerStats.player_id == player_id)
            ).first()[0]

            stats.games_won += 1
            stats.score += points

            conn.commit()
            return stats.score

    def player_started_new_game(self, player_id: int, new_solution: str):
        with self._engine.connect() as conn:
            stmt = (
                update(Player)
                .where(Player.id == player_id)
                .values(active_solution=new_solution)
            )
            conn.execute(stmt)

            stmt = (
                update(PlayerStats)
                .where(PlayerStats.player_id == player_id)
                .values(games_played=PlayerStats.games_played + 1)
            )
            conn.execute(stmt)

            conn.commit()
