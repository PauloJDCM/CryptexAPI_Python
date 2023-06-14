import os
from sqlalchemy import create_engine, insert
from data.cryptexmodels import Base, User, Leaderboard, ActivePuzzle


class CryptexDB:
    def __init__(self):
        self._engine = create_engine(
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@db:5432/postgres", echo=True)
        Base.metadata.create_all(self._engine)

    def register_user(self, external_id: str, name: str):
        with self._engine.connect() as conn:
            user_stmt = insert(User).values(external_id=external_id, name=name)
            user_id = conn.execute(user_stmt).inserted_primary_key[0]

            lead_stmt = insert(Leaderboard).values(user_id=user_id, score=0)
            puzzle_stmt = insert(ActivePuzzle).values(user_id=user_id)

            conn.execute(lead_stmt)
            conn.execute(puzzle_stmt)

            conn.commit()
