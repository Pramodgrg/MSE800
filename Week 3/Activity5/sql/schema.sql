-- ============================================================
-- Money Exchange System — Database Schema
-- Engine: SQLite (portable to PostgreSQL/MySQL with minor tweaks)
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- 1. customers
-- Every exchange transaction must be tied to a real, identifiable
-- person (KYC requirement in currency exchange businesses).
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    customer_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT UNIQUE,
    phone           TEXT,
    national_id     TEXT UNIQUE NOT NULL,   -- passport / ID number, required for KYC/AML
    address         TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ------------------------------------------------------------
-- 2. currencies
-- A lookup/reference table of every currency the business trades.
-- Kept separate so currency data (code, symbol, decimal places)
-- is defined once and referenced everywhere else by ID, instead
-- of being repeated as free text in every rate/transaction row.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS currencies (
    currency_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    code            TEXT NOT NULL UNIQUE,     -- ISO 4217, e.g. USD, EUR, NZD
    name            TEXT NOT NULL,            -- e.g. "United States Dollar"
    symbol          TEXT NOT NULL,            -- e.g. "$"
    decimal_places  INTEGER NOT NULL DEFAULT 2,
    is_active       INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1))
);

-- ------------------------------------------------------------
-- 3. exchange_rates
-- Rates change over time and depend on a currency PAIR, so this
-- must be its own table (a many-to-many relationship between
-- currencies, with a rate + timestamp as attributes of that
-- relationship). Historical rates are preserved for auditing.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS exchange_rates (
    rate_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    from_currency_id    INTEGER NOT NULL,
    to_currency_id      INTEGER NOT NULL,
    rate                REAL NOT NULL CHECK (rate > 0),
    effective_date      TEXT NOT NULL DEFAULT (datetime('now')),
    created_at          TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (from_currency_id) REFERENCES currencies(currency_id),
    FOREIGN KEY (to_currency_id)   REFERENCES currencies(currency_id),
    CHECK (from_currency_id <> to_currency_id)
);

-- ------------------------------------------------------------
-- 4. transactions
-- The core business event: a customer exchanging one currency
-- for another. Stores the amounts and the rate actually used at
-- the time of the trade (never recomputed from exchange_rates
-- later, so historical transactions stay accurate even if rates
-- change afterward).
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id         INTEGER NOT NULL,
    from_currency_id    INTEGER NOT NULL,
    to_currency_id      INTEGER NOT NULL,
    from_amount         REAL NOT NULL CHECK (from_amount > 0),
    to_amount           REAL NOT NULL CHECK (to_amount > 0),
    rate_used            REAL NOT NULL CHECK (rate_used > 0),
    transaction_date    TEXT NOT NULL DEFAULT (datetime('now')),
    status               TEXT NOT NULL DEFAULT 'COMPLETED'
                          CHECK (status IN ('PENDING','COMPLETED','CANCELLED')),
    FOREIGN KEY (customer_id)      REFERENCES customers(customer_id),
    FOREIGN KEY (from_currency_id) REFERENCES currencies(currency_id),
    FOREIGN KEY (to_currency_id)   REFERENCES currencies(currency_id)
);

CREATE INDEX IF NOT EXISTS idx_rates_pair ON exchange_rates(from_currency_id, to_currency_id, effective_date);
CREATE INDEX IF NOT EXISTS idx_tx_customer ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_tx_date ON transactions(transaction_date);
