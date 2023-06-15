import os
from sqlalchemy import create_engine, insert
from data.cryptexmodels import Base, Player, PlayerStats


class CryptexDB:
    def __init__(self):
        self._engine = create_engine(
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@db:5432/postgres", echo=True)
        Base.metadata.create_all(self._engine)

    def register_player(self, external_id: str, name: str):
        with self._engine.connect() as conn:
            user_stmt = insert(Player).values(external_id=external_id, name=name)
            user_id = conn.execute(user_stmt).inserted_primary_key[0]

            stats_stmt = insert(PlayerStats).values(user_id=user_id, games_played=0, games_won=0, score=0)
            conn.execute(stats_stmt)

            conn.commit()
