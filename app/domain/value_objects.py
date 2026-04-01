from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


@dataclass
class Money:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money cannot be negative")

    def __add__(self, other: "Money") -> "Money":
        """Сложение двух Money объектов.

        Raises:
            ValueError: Если валюты не совпадают.
        """
        if self.currency != other.currency:
            raise ValueError("Cannot operate on different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        """Вычитание двух Money объектов.

        Raises:
            ValueError: Если валюты не совпадают.
        """
        if self.currency != other.currency:
            raise ValueError("Cannot operate on different currencies")
        return Money(self.amount - other.amount, self.currency)

    def __lt__(self, other: "Money") -> bool:
        """Меньше чем (<)."""
        if self.currency != other.currency:
            raise ValueError("Cannot operate on different currencies")
        return self.amount < other.amount

    def __le__(self, other: "Money") -> bool:
        """Меньше или равно (<=)."""
        if self.currency != other.currency:
            raise ValueError("Cannot operate on different currencies")
        return self.amount <= other.amount

    def __gt__(self, other: "Money") -> bool:
        """Больше чем (>)."""
        if self.currency != other.currency:
            raise ValueError("Cannot operate on different currencies")
        return self.amount > other.amount

    def __ge__(self, other: "Money") -> bool:
        """Больше или равно (>=)."""
        if self.currency != other.currency:
            raise ValueError("Cannot operate on different currencies")
        return self.amount >= other.amount

    def __eq__(self, other: object) -> bool:
        """Равенство (==)."""
        if not isinstance(other, Money):
            return False
        if self.currency != other.currency:
            raise ValueError("Cannot operate on different currencies")
        return self.amount == other.amount and self.currency == other.currency


class AuctionStatus(Enum):
    CREATED = "Auction created"
    ACTIVE = "Auction is active"
    COMPLETED = "Auction completed"
    CANCELED = "Auction canceled"
