-- =============================================
-- Schema PostgreSQL para Sistema Inmobiliario
-- Ejecutar en Supabase > SQL Editor
-- =============================================

CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    last_name   VARCHAR(100),
    email       VARCHAR(100) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    tel         VARCHAR(20),
    role        VARCHAR(10) NOT NULL DEFAULT 'cliente',
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lots (
    id          SERIAL PRIMARY KEY,
    area        INT NOT NULL,
    location    VARCHAR(100) NOT NULL,
    price       DECIMAL(10, 2) NOT NULL,
    stage       VARCHAR(50),
    status      VARCHAR(20) NOT NULL DEFAULT 'disponible',
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS purchases (
    id            SERIAL PRIMARY KEY,
    user_id       INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lot_id        INT NOT NULL REFERENCES lots(id) ON DELETE CASCADE,
    purchase_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payments (
    id            SERIAL PRIMARY KEY,
    purchase_id   INT NOT NULL REFERENCES purchases(id) ON DELETE CASCADE,
    amount        DECIMAL(10, 2) NOT NULL,
    payment_date  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pqrs (
    id          SERIAL PRIMARY KEY,
    user_id     INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type        VARCHAR(50) NOT NULL,
    message     TEXT NOT NULL,
    status      VARCHAR(50) NOT NULL DEFAULT 'pendiente',
    created_at  TIMESTAMP DEFAULT NOW()
);
