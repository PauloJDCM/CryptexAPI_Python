import os
from sqlalchemy import create_engine, insert, update, select
from sqlalchemy.orm import Session

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

    def player_won(self, external_id: str, points: int) -> int:
        with Session(self._engine) as session:
            player_id = self._get_player_id(session, external_id)

            stats = session.execute(
                select(PlayerStats)
                .where(PlayerStats.player_id == player_id)
            ).first()[0]

            stats.games_won += 1
            stats.score += points

            session.commit()
            return stats.score

    def player_started_new_game(self, external_id: str, new_solution: str):
        with Session(self._engine) as session:
            player_id = self._get_player_id(session, external_id)

            stmt = (
                update(Player)
                .where(Player.id == player_id)
                .values(active_solution=new_solution)
            )
            session.execute(stmt)

            stmt = (
                update(PlayerStats)
                .where(PlayerStats.player_id == player_id)
                .values(games_played=PlayerStats.games_played + 1)
            )
            session.execute(stmt)

            session.commit()

    @staticmethod
    def _get_player_id(session: Session, external_id: str) -> int:
        stmt = select(Player.id).where(Player.external_id == external_id)

        return session.execute(stmt).first()[0]
