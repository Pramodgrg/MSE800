"""
models.py
---------
Plain OOP domain objects for the Money Exchange System.

Each class mirrors one database table and is responsible only for
representing/validating its own data (no SQL here — persistence is
handled separately by the Repository classes in database.py).
This keeps the "domain model" cleanly separated from "data access",
following the Single Responsibility Principle.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    first_name: str
    last_name: str
    national_id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    customer_id: Optional[int] = None
    created_at: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"Customer#{self.customer_id} {self.full_name} ({self.national_id})"


@dataclass
class Currency:
    code: str            # ISO 4217, e.g. "USD"
    name: str
    symbol: str
    decimal_places: int = 2
    is_active: bool = True
    currency_id: Optional[int] = None

    def __post_init__(self):
        self.code = self.code.upper().strip()

    def format_amount(self, amount: float) -> str:
        return f"{self.symbol}{amount:,.{self.decimal_places}f}"

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


@dataclass
class ExchangeRate:
    from_currency_id: int
    to_currency_id: int
    rate: float
    rate_id: Optional[int] = None
    effective_date: Optional[str] = None
    created_at: Optional[str] = None

    def convert(self, amount: float) -> float:
        """Convert an amount in the 'from' currency to the 'to' currency."""
        if amount <= 0:
            raise ValueError("Amount to convert must be positive.")
        return round(amount * self.rate, 4)

    def __str__(self) -> str:
        return f"Rate#{self.rate_id}: 1 unit -> {self.rate} (as of {self.effective_date})"


@dataclass
class Transaction:
    customer_id: int
    from_currency_id: int
    to_currency_id: int
    from_amount: float
    to_amount: float
    rate_used: float
    transaction_id: Optional[int] = None
    transaction_date: Optional[str] = None
    status: str = "COMPLETED"

    VALID_STATUSES = ("PENDING", "COMPLETED", "CANCELLED")

    def __post_init__(self):
        if self.status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{self.status}'. Must be one of {self.VALID_STATUSES}")
        if self.from_amount <= 0 or self.to_amount <= 0:
            raise ValueError("Transaction amounts must be positive.")

    def cancel(self):
        self.status = "CANCELLED"

    def __str__(self) -> str:
        return (f"Transaction#{self.transaction_id} customer={self.customer_id} "
                f"{self.from_amount} -> {self.to_amount} @ {self.rate_used} [{self.status}]")
