"""
Basic tests for the Money Exchange System (stdlib unittest — no
external dependencies required).

Run with: python3 -m unittest discover -s tests -v   (from project root)
"""

import sys
import unittest
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from database import Database, ExchangeService
from models import Customer, Currency, ExchangeRate, Transaction


class ExchangeSystemTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        db_file = str(Path(self._tmpdir.name) / "test.db")
        self.db = Database(db_file)
        self.db.init_schema()
        self.service = ExchangeService(self.db)

        self.usd = self.service.currencies.create(Currency(code="USD", name="US Dollar", symbol="$"))
        self.eur = self.service.currencies.create(Currency(code="EUR", name="Euro", symbol="\u20ac"))
        self.service.rates.create(
            ExchangeRate(from_currency_id=self.usd.currency_id, to_currency_id=self.eur.currency_id, rate=0.9)
        )

    def tearDown(self):
        self.db.close()
        self._tmpdir.cleanup()

    def test_create_customer(self):
        c = self.service.customers.create(Customer(first_name="Jane", last_name="Doe", national_id="ID001"))
        self.assertIsNotNone(c.customer_id)
        fetched = self.service.customers.get(c.customer_id)
        self.assertEqual(fetched.full_name, "Jane Doe")

    def test_exchange_success(self):
        c = self.service.customers.create(Customer(first_name="Jane", last_name="Doe", national_id="ID002"))
        tx = self.service.exchange(customer_id=c.customer_id, from_code="USD", to_code="EUR", from_amount=100)
        self.assertEqual(tx.to_amount, 90.0)
        self.assertEqual(tx.status, "COMPLETED")

    def test_exchange_missing_rate_raises(self):
        c = self.service.customers.create(Customer(first_name="Jane", last_name="Doe", national_id="ID003"))
        with self.assertRaises(ValueError):
            self.service.exchange(customer_id=c.customer_id, from_code="EUR", to_code="USD", from_amount=50)

    def test_transaction_rejects_negative_amount(self):
        with self.assertRaises(ValueError):
            Transaction(customer_id=1, from_currency_id=1, to_currency_id=2,
                        from_amount=-10, to_amount=5, rate_used=0.5)


if __name__ == "__main__":
    unittest.main()
