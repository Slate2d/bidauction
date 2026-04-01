from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    balance = Column(DECIMAL(12,2), nullable=False)
    frozen_balance = Column(DECIMAL(12,2), nullable=False)

class AuctionModel(Base):
    __tablename__ = "auctions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    start_price = Column(DECIMAL(12, 2), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    description = Column(String, nullable=False)
    min_step = Column(DECIMAL(10,2), nullable=False)
    current_price = Column(DECIMAL(12,2), nullable=False)
    leader_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status = Column(String, nullable=False)
    end_time = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

class BidModel(Base):
    __tablename__ = "bids"

    id = Column(UUID(as_uuid=True), primary_key=True)
    auction_id = Column(UUID(as_uuid=True), ForeignKey("auctions.id"), index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(DECIMAL(12,2), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )