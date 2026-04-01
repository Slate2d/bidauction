from uuid import UUID
from dataclasses import dataclass
from app.domain.value_objects import Money
from app.domain.exceptions import InsufficientFundsError


@dataclass
class User:
    id: UUID
    email: str
    password_hash: str
    balance: Money
    frozen_balance: Money

    @property
    def available_balance(self) -> Money:
        return self.balance - self.frozen_balance

    def can_afford(self, money: Money) -> bool:
        return self.available_balance >= money

    def deposit(self, money: Money) -> None:
        """Пополнить баланс пользователя."""
        self.balance = self.balance + money

    def freeze_funds(self, money: Money) -> None:
        """Заморозить средства под ставку.
            Raises:
            InsufficientFundsError: Если недостаточно доступных средств.
        """
        if self.available_balance < money:
            raise InsufficientFundsError
        self.frozen_balance = money + self.frozen_balance

    def unfreeze_funds(self, amount: Money) -> None:
        """Разморозить средства (когда ставку перебили)."""
        self.frozen_balance = self.frozen_balance - amount
