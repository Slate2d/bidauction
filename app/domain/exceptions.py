from decimal import Decimal


class DomainException(Exception):
    pass


class BidTooLowError(DomainException):
    def __init__(self, min_required: Decimal, current_price: Decimal):
        self.min_required = min_required
        self.current_price = current_price
        super().__init__(
            f"Минимальная сумма ставки должна быть {min_required}")


class InsufficientFundsError(DomainException):
    def __init__(self, required_amount: Decimal, available_balance: Decimal):
        self.required_amount = required_amount
        self.available_balance = available_balance
        super().__init__(
            f"Доступно на балансе {available_balance}, а нужно {required_amount}")


class AuctionNotActiveError(DomainException):
    pass


class AuctionEndedError(DomainException):
    pass


class UnauthorizedError(DomainException):
    pass
