"""
database.py
-----------
OOP data-access layer for the Money Exchange System.

Design:
- Database: owns the sqlite3 connection and schema creation.
- BaseRepository: shared plumbing (row -> object mapping helpers).
- CustomerRepository / CurrencyRepository / ExchangeRateRepository /
  TransactionRepository: one repository per table, each exposing
  create/get/list/update methods for its entity (Repository pattern).
- ExchangeService: business-logic layer that composes the repositories
  to perform a full currency exchange (look up latest rate, compute
  amount, record the transaction) as a single unit of work.
"""

import sqlite3
from pathlib import Path
from typing import List, Optional

from models import Customer, Currency, ExchangeRate, Transaction

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"


class Database:
    """Owns the connection and schema lifecycle."""

    def __init__(self, db_path: str = "exchange.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.row_factory = sqlite3.Row

    def init_schema(self):
        sql = SCHEMA_PATH.read_text()
        self.conn.executescript(sql)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class BaseRepository:
    def __init__(self, db: Database):
        self.db = db
        self.conn = db.conn


class CustomerRepository(BaseRepository):
    def create(self, customer: Customer) -> Customer:
        cur = self.conn.execute(
            """INSERT INTO customers (first_name, last_name, email, phone, national_id, address)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (customer.first_name, customer.last_name, customer.email,
             customer.phone, customer.national_id, customer.address),
        )
        self.conn.commit()
        customer.customer_id = cur.lastrowid
        return customer

    def get(self, customer_id: int) -> Optional[Customer]:
        row = self.conn.execute(
            "SELECT * FROM customers WHERE customer_id = ?", (customer_id,)
        ).fetchone()
        return self._row_to_customer(row) if row else None

    def list_all(self) -> List[Customer]:
        rows = self.conn.execute("SELECT * FROM customers ORDER BY customer_id").fetchall()
        return [self._row_to_customer(r) for r in rows]

    @staticmethod
    def _row_to_customer(row: sqlite3.Row) -> Customer:
        return Customer(
            customer_id=row["customer_id"], first_name=row["first_name"],
            last_name=row["last_name"], email=row["email"], phone=row["phone"],
            national_id=row["national_id"], address=row["address"],
            created_at=row["created_at"],
        )


class CurrencyRepository(BaseRepository):
    def create(self, currency: Currency) -> Currency:
        cur = self.conn.execute(
            """INSERT INTO currencies (code, name, symbol, decimal_places, is_active)
               VALUES (?, ?, ?, ?, ?)""",
            (currency.code, currency.name, currency.symbol,
             currency.decimal_places, int(currency.is_active)),
        )
        self.conn.commit()
        currency.currency_id = cur.lastrowid
        return currency

    def get_by_code(self, code: str) -> Optional[Currency]:
        row = self.conn.execute(
            "SELECT * FROM currencies WHERE code = ?", (code.upper(),)
        ).fetchone()
        return self._row_to_currency(row) if row else None

    def list_all(self) -> List[Currency]:
        rows = self.conn.execute("SELECT * FROM currencies ORDER BY code").fetchall()
        return [self._row_to_currency(r) for r in rows]

    @staticmethod
    def _row_to_currency(row: sqlite3.Row) -> Currency:
        return Currency(
            currency_id=row["currency_id"], code=row["code"], name=row["name"],
            symbol=row["symbol"], decimal_places=row["decimal_places"],
            is_active=bool(row["is_active"]),
        )


class ExchangeRateRepository(BaseRepository):
    def create(self, rate: ExchangeRate) -> ExchangeRate:
        cur = self.conn.execute(
            """INSERT INTO exchange_rates (from_currency_id, to_currency_id, rate)
               VALUES (?, ?, ?)""",
            (rate.from_currency_id, rate.to_currency_id, rate.rate),
        )
        self.conn.commit()
        rate.rate_id = cur.lastrowid
        return rate

    def get_latest(self, from_currency_id: int, to_currency_id: int) -> Optional[ExchangeRate]:
        row = self.conn.execute(
            """SELECT * FROM exchange_rates
               WHERE from_currency_id = ? AND to_currency_id = ?
               ORDER BY effective_date DESC, rate_id DESC LIMIT 1""",
            (from_currency_id, to_currency_id),
        ).fetchone()
        return self._row_to_rate(row) if row else None

    def history(self, from_currency_id: int, to_currency_id: int) -> List[ExchangeRate]:
        rows = self.conn.execute(
            """SELECT * FROM exchange_rates
               WHERE from_currency_id = ? AND to_currency_id = ?
               ORDER BY effective_date DESC""",
            (from_currency_id, to_currency_id),
        ).fetchall()
        return [self._row_to_rate(r) for r in rows]

    @staticmethod
    def _row_to_rate(row: sqlite3.Row) -> ExchangeRate:
        return ExchangeRate(
            rate_id=row["rate_id"], from_currency_id=row["from_currency_id"],
            to_currency_id=row["to_currency_id"], rate=row["rate"],
            effective_date=row["effective_date"], created_at=row["created_at"],
        )


class TransactionRepository(BaseRepository):
    def create(self, tx: Transaction) -> Transaction:
        cur = self.conn.execute(
            """INSERT INTO transactions
               (customer_id, from_currency_id, to_currency_id, from_amount, to_amount, rate_used, status)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (tx.customer_id, tx.from_currency_id, tx.to_currency_id,
             tx.from_amount, tx.to_amount, tx.rate_used, tx.status),
        )
        self.conn.commit()
        tx.transaction_id = cur.lastrowid
        return tx

    def list_for_customer(self, customer_id: int) -> List[Transaction]:
        rows = self.conn.execute(
            "SELECT * FROM transactions WHERE customer_id = ? ORDER BY transaction_date DESC",
            (customer_id,),
        ).fetchall()
        return [self._row_to_tx(r) for r in rows]

    def list_all(self) -> List[Transaction]:
        rows = self.conn.execute("SELECT * FROM transactions ORDER BY transaction_date DESC").fetchall()
        return [self._row_to_tx(r) for r in rows]

    @staticmethod
    def _row_to_tx(row: sqlite3.Row) -> Transaction:
        return Transaction(
            transaction_id=row["transaction_id"], customer_id=row["customer_id"],
            from_currency_id=row["from_currency_id"], to_currency_id=row["to_currency_id"],
            from_amount=row["from_amount"], to_amount=row["to_amount"],
            rate_used=row["rate_used"], transaction_date=row["transaction_date"],
            status=row["status"],
        )


class ExchangeService:
    """
    Business-logic facade: composes the repositories to perform a
    full currency exchange as one operation, so callers don't need
    to know about rate look-ups and transaction bookkeeping.
    """

    def __init__(self, db: Database):
        self.db = db
        self.customers = CustomerRepository(db)
        self.currencies = CurrencyRepository(db)
        self.rates = ExchangeRateRepository(db)
        self.transactions = TransactionRepository(db)

    def exchange(self, customer_id: int, from_code: str, to_code: str, from_amount: float) -> Transaction:
        from_currency = self.currencies.get_by_code(from_code)
        to_currency = self.currencies.get_by_code(to_code)
        if not from_currency or not to_currency:
            raise ValueError("Unknown currency code.")

        rate = self.rates.get_latest(from_currency.currency_id, to_currency.currency_id)
        if not rate:
            raise ValueError(f"No exchange rate available for {from_code} -> {to_code}.")

        to_amount = rate.convert(from_amount)

        tx = Transaction(
            customer_id=customer_id,
            from_currency_id=from_currency.currency_id,
            to_currency_id=to_currency.currency_id,
            from_amount=from_amount,
            to_amount=to_amount,
            rate_used=rate.rate,
        )
        return self.transactions.create(tx)
