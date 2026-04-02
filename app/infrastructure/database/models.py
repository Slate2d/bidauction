from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, DECIMAL, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID as PyUUID

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    balance: Mapped[Decimal] = mapped_column(DECIMAL(12, 2))
    frozen_balance: Mapped[Decimal] = mapped_column(DECIMAL(12, 2))

class AuctionModel(Base):
    __tablename__ = "auctions"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    seller_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String)
    start_price: Mapped[Decimal] = mapped_column(DECIMAL(12, 2))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    description: Mapped[str] = mapped_column(String)
    min_step: Mapped[Decimal] = mapped_column(DECIMAL(10,2))
    current_price: Mapped[Decimal] = mapped_column(DECIMAL(12,2))
    leader_id: Mapped[PyUUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String)
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True
    )

class BidModel(Base):
    __tablename__ = "bids"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    auction_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("auctions.id"), index=True)
    user_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(12,2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )