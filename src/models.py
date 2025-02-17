from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(80))
    name: Mapped[str] = mapped_column(String(80),nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool]
    favorites: Mapped[List["Favorites"]] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,
            "is_active": self.is_active
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    diameter: Mapped[str] = mapped_column(nullable=False)
    gravity: Mapped[str] = mapped_column(nullable=False)
    favorites: Mapped[List["Favorites"]] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity
        }
class People(db.Model):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    eyes_color: Mapped[str] = mapped_column(nullable=False)
    hair_color: Mapped[str] = mapped_column(nullable=False)
    heigth: Mapped[str] = mapped_column(nullable=False)
    favorites: Mapped[List["Favorites"]] = relationship()
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eyes_color": self.eyes_color,
            "hair_color": self.hair_color,
            "heigth": self.heigth
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
        }
