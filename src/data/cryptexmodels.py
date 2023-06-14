from typing_extensions import Annotated
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, MappedAsDataclass

uuid_type = Annotated[str, 36]
username_type = Annotated[str, 25]
solution_type = Annotated[str, 35]


class Base(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {
        uuid_type: String(36),
        username_type: String(25),
        solution_type: String(35)
    }


class ActivePuzzle(Base):
    __tablename__ = "active_puzzles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"))
    solution: Mapped[solution_type] = mapped_column(nullable=True)


class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"))
    score: Mapped[int]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[uuid_type]
    name: Mapped[username_type]
    active_puzzle: Mapped[ActivePuzzle] = relationship()
    score: Mapped[Leaderboard] = relationship()
