from app.domain.entities.user import User
from app.infrastructure.database.models import UserModel
from app.domain.value_objects import Money
from decimal import Decimal
from app.domain.entities.auction import Auction
from app.domain.entities.bid import Bid
from app.infrastructure.database.models import AuctionModel, BidModel
from app.domain.value_objects import AuctionStatus

def auction_to_domain(model: AuctionModel) -> Auction:
    return Auction(
        id=model.id,
        seller_id=model.seller_id,
        title=model.title,
        min_step=Money(amount=model.min_step, currency="USD"),
        current_price=Money(amount=model.current_price, currency="USD"),
        start_price=Money(amount=model.start_price, currency="USD"),
        start_time=model.start_time,
        description=model.description,
        leader_id=model.leader_id,
        status=AuctionStatus[model.status],
        end_time=model.end_time
    )

def auction_to_orm(entity: Auction) -> AuctionModel:
    return AuctionModel(
        id=entity.id,
        seller_id=entity.seller_id,
        title=entity.title,
        min_step=entity.min_step.amount,
        current_price=entity.current_price.amount,
        start_price=entity.start_price.amount,
        start_time=entity.start_time,
        description=entity.description,
        leader_id=entity.leader_id,
        status=entity.status.name,
        end_time=entity.end_time
    )

def bid_to_domain(model: BidModel) -> Bid:
    """Конвертировать ORM модель в Domain Entity."""
    return Bid(
        id = model.id,
        auction_id = model.auction_id,
        user_id = model.user_id,
        amount = Money(amount=model.amount, currency="USD"),
        created_at = model.created_at
    )

def bid_to_orm(entity: Bid) -> BidModel:
    """Конвертировать Domain Entity в ORM модель."""
    return BidModel(
        id = entity.id,
        auction_id = entity.auction_id,
        user_id = entity.user_id,
        amount = entity.amount.amount,
        created_at = entity.created_at
    )

def user_to_domain(model: UserModel) -> User:
    """Конвертировать ORM модель в Domain Entity.

    Args:
        model: SQLAlchemy UserModel из БД

    Returns:
        User domain entity
    """
    return User(
        id=model.id,
        email=model.email,
        password_hash=model.password_hash,
        balance=Money(amount=model.balance, currency="USD"),
        frozen_balance=Money(amount=model.frozen_balance, currency="USD")
    )


def user_to_orm(entity: User) -> UserModel:
    """Конвертировать Domain Entity в ORM модель.

    Args:
        entity: User domain entity

    Returns:
        SQLAlchemy UserModel для сохранения в БД
    """
    return UserModel(
        id=entity.id,
        email=entity.email,
        password_hash=entity.password_hash,
        balance=entity.balance.amount,
        frozen_balance=entity.frozen_balance.amount
    )