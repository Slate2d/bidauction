from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    # TODO: Добавь колонки согласно документации (строки 76-86)
    # Подсказка: используй UUID для id, String для email, DECIMAL(12,2) для балансов
    pass


class AuctionModel(Base):
    __tablename__ = "auctions"

    # TODO: Добавь колонки согласно документации (строки 94-107)
    # Не забудь про ForeignKey на users.id для seller_id и leader_id
    pass


class BidModel(Base):
    __tablename__ = "bids"

    # TODO: Добавь колонки согласно документации (строки 112-122)
    # Не забудь про ForeignKey на auctions.id и users.id
    pass