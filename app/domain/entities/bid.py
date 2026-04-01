from uuid import UUID
from dataclasses import dataclass
from datetime import datetime
from app.domain.value_objects import Money


@dataclass
class Bid:
    id: UUID
    auction_id: UUID
    user_id: UUID
    amount: Money
    created_at: datetime
