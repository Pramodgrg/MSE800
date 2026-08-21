"""
demo.py
-------
Seeds the database with sample data and demonstrates the full
OOP workflow: create customers/currencies/rates, then perform
an exchange transaction through ExchangeService.

Run with:  python3 src/demo.py
"""

from pathlib import Path

from database import Database, ExchangeService
from models import Customer, Currency, ExchangeRate

DB_FILE = str(Path(__file__).resolve().parent.parent / "exchange.db")


def seed(service: ExchangeService):
    # -- currencies --
    usd = service.currencies.create(Currency(code="USD", name="US Dollar", symbol="$"))
    eur = service.currencies.create(Currency(code="EUR", name="Euro", symbol="\u20ac"))
    nzd = service.currencies.create(Currency(code="NZD", name="New Zealand Dollar", symbol="$"))

    # -- exchange rates (1 unit of `from` -> `to`) --
    service.rates.create(ExchangeRate(from_currency_id=usd.currency_id, to_currency_id=eur.currency_id, rate=0.92))
    service.rates.create(ExchangeRate(from_currency_id=usd.currency_id, to_currency_id=nzd.currency_id, rate=1.66))
    service.rates.create(ExchangeRate(from_currency_id=eur.currency_id, to_currency_id=usd.currency_id, rate=1.087))

    # -- customers --
    alice = service.customers.create(
        Customer(first_name="Alice", last_name="Nguyen", national_id="P1234567", email="alice@example.com")
    )
    bob = service.customers.create(
        Customer(first_name="Bob", last_name="Smith", national_id="P7654321", email="bob@example.com")
    )
    return alice, bob


def main():
    Path(DB_FILE).unlink(missing_ok=True)  # fresh demo run each time
    with Database(DB_FILE) as db:
        db.init_schema()
        service = ExchangeService(db)

        alice, bob = seed(service)

        print("=== Currencies ===")
        for c in service.currencies.list_all():
            print(" ", c)

        print("\n=== Customers ===")
        for c in service.customers.list_all():
            print(" ", c)

        print("\n=== Performing exchange: Alice converts 500 USD -> EUR ===")
        tx = service.exchange(customer_id=alice.customer_id, from_code="USD", to_code="EUR", from_amount=500)
        print(" ", tx)

        print("\n=== Performing exchange: Bob converts 200 USD -> NZD ===")
        tx2 = service.exchange(customer_id=bob.customer_id, from_code="USD", to_code="NZD", from_amount=200)
        print(" ", tx2)

        print("\n=== All transactions ===")
        for t in service.transactions.list_all():
            print(" ", t)


if __name__ == "__main__":
    main()
