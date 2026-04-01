from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from app.domain.value_objects import AuctionStatus
from app.domain.value_objects import Money
from app.domain.exceptions import BidTooLowError, AuctionNotActiveError


@dataclass
class Auction:
    id: UUID
    seller_id: UUID
    title: str
    min_step: Money
    current_price: Money
    start_price: Money
    start_time: datetime
    description: str
    leader_id: UUID | None
    status: AuctionStatus
    end_time: datetime

    def can_accept_bid(self, money: Money) -> bool:
        return money >= self.current_price + self.min_step

    def place_bid(self, user_id: UUID, money: Money) -> None:
        """Принять новую ставку.

        Raises:
            AuctionNotActiveError: Если аукцион не в статусе ACTIVE.
            BidTooLowError: Если ставка меньше current_price + min_step.
        """
        if self.status is not AuctionStatus.ACTIVE:
            raise AuctionNotActiveError
        if not self.can_accept_bid(money):
            raise BidTooLowError
        self.current_price = money
        self.leader_id = user_id

    def close(self) -> None:
        """Закрыть аукцион. Победитель — текущий leader_id."""
        self.status = AuctionStatus.COMPLETED

    def cancel(self) -> None:
        self.status = AuctionStatus.CANCELED
