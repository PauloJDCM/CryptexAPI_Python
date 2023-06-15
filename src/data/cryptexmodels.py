from typing_extensions import Annotated
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, MappedAsDataclass

uuid_type = Annotated[str, 36]
playername_type = Annotated[str, 25]
solution_type = Annotated[str, 35]


class Base(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {
        uuid_type: String(36),
        playername_type: String(25),
        solution_type: String(35)
    }


class PlayerStats(Base):
    __tablename__ = "player_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id = mapped_column(ForeignKey("players.id"))
    games_played: Mapped[int]
    games_won: Mapped[int]
    score: Mapped[int]


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[uuid_type]
    name: Mapped[playername_type]
    active_solution: Mapped[solution_type] = mapped_column(nullable=True)
    stats: Mapped[PlayerStats] = relationship()
