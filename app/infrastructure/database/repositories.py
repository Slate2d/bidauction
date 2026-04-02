from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from datetime import datetime

from app.interfaces.repositories import (
    UserRepository,
    AuctionRepository,
    BidRepository
)
from app.domain.entities.user import User
from app.domain.entities.auction import Auction
from app.domain.entities.bid import Bid
from app.domain.value_objects import AuctionStatus
from app.infrastructure.database.models import UserModel, AuctionModel, BidModel
from app.infrastructure.database.mappers import (
    user_to_domain, user_to_orm,
    auction_to_domain, auction_to_orm,
    bid_to_domain, bid_to_orm
)

class SQLAlchemyUserRepository(UserRepository):
    """Реализация UserRepository через SQLAlchemy."""

    def __init__(self, session: Session):
        """
        Args:
            session: SQLAlchemy session для работы с БД
        """
        self.session = session

    def save(self, user: User) -> None:
        """Сохранить или обновить пользователя."""
        orm_user = user_to_orm(user)
        self.session.merge(orm_user)
        self.session.flush()

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Получить пользователя по ID."""
        model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if model is None:
            return None
        return user_to_domain(model)

    def get_by_email(self, email: str) -> Optional[User]:
        """Получить пользователя по email."""
        model = self.session.query(UserModel).filter(UserModel.email == email).first()
        if model is None:
            return None
        return user_to_domain(model)




class SQLAlchemyAuctionRepository(AuctionRepository):
    """Реализация AuctionRepository через SQLAlchemy."""

    def __init__(self, session: Session):
        self.session = session

    def save(self, auction: Auction) -> None:
        """Сохранить или обновить аукцион."""
        orm_auction = auction_to_orm(auction)
        self.session.merge(orm_auction)
        self.session.flush()

    def get_by_id(self, auction_id: UUID) -> Optional[Auction]:
        """Получить аукцион по ID."""
        model = self.session.query(AuctionModel).filter(AuctionModel.id == auction_id).first()
        if model is None:
            return None
        return auction_to_domain(model)

    def get_active_expired(self, current_time: datetime) -> list[Auction]:
        """Получить активные аукционы, у которых истекло время.

        Этот метод используется Celery worker'ом для закрытия аукционов.
        """
        models = self.session.query(AuctionModel).filter(
            AuctionModel.status == AuctionStatus.ACTIVE.name,
            AuctionModel.end_time <= current_time
        ).all()
        return [auction_to_domain(m) for m in models]

    def get_by_id_for_update(self, auction_id: UUID) -> Optional[Auction]:
        """Get auction with pessimistic lock for concurrent bid handling."""
        model = self.session.query(AuctionModel).filter(
            AuctionModel.id == auction_id
        ).with_for_update().first()
        if model is None:
            return None
        return auction_to_domain(model)


class SQLAlchemyBidRepository(BidRepository):
    """Реализация BidRepository через SQLAlchemy."""

    def __init__(self, session: Session):
        self.session = session

    def save(self, bid: Bid) -> None:
        """Сохранить ставку."""
        orm_bid = bid_to_orm(bid)
        self.session.merge(orm_bid)
        self.session.flush()

    def get_by_auction_id(self, auction_id: UUID) -> list[Bid]:
        """Получить все ставки для аукциона (для истории)."""
        models = self.session.query(BidModel).filter(
            BidModel.auction_id == auction_id
        ).order_by(BidModel.created_at.desc()).all()
        return [bid_to_domain(m) for m in models]