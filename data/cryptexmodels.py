from typing_extensions import Annotated
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, MappedAsDataclass

uuid = Annotated[str, 36]
username = Annotated[str, 25]
solutionid = Annotated[str, 5]


class Base(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {
        uuid: String(36),
        username: String(25),
        solutionid: String(5)
    }


class User(Base):
    __tablename__ = "Users"

    Id: Mapped[int] = mapped_column(primary_key=True)
    ExternalId: Mapped[uuid]
    Name: Mapped[username]
    ActivePuzzle: Mapped["ActivePuzzle"] = relationship()
    Score: Mapped["Leaderboard"] = relationship()


class ActivePuzzle(Base):
    __tablename__ = "ActivePuzzles"

    Id: Mapped[int] = mapped_column(primary_key=True)
    UserId = mapped_column(ForeignKey("Users.Id"))
    Solution: Mapped[solutionid] = mapped_column(nullable=True)


class Leaderboard(Base):
    __tablename__ = "Leaderboard"

    Id: Mapped[int] = mapped_column(primary_key=True)
    UserId = mapped_column(ForeignKey("Users.Id"))
    Score: Mapped[int]
