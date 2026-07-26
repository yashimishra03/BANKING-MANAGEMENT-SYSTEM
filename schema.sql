-- ============================================================
-- Banking Management System - MySQL Schema
-- Subject: Design and Analysis of Algorithms (DAA)
-- ============================================================

CREATE DATABASE IF NOT EXISTS banking_system;
USE banking_system;

-- ---------------------------------------------------------
-- Customers table (backing store for the Linked List / BST)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    customer_id     INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100)  NOT NULL,
    email           VARCHAR(100)  NOT NULL UNIQUE,
    phone           VARCHAR(15)   NOT NULL,
    password_hash   VARCHAR(255)  NOT NULL,
    balance         DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------
-- Transactions table (backing store for the Stack)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id  INT AUTO_INCREMENT PRIMARY KEY,
    customer_id     INT NOT NULL,
    type            ENUM('deposit', 'withdraw', 'transfer_out', 'transfer_in') NOT NULL,
    amount          DECIMAL(15,2) NOT NULL,
    balance_after   DECIMAL(15,2) NOT NULL,
    related_customer_id INT DEFAULT NULL,   -- used for transfers
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- ---------------------------------------------------------
-- Requests table (backing store for the Queue)
-- e.g. cheque book request, statement request, card block, etc.
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS requests (
    request_id      INT AUTO_INCREMENT PRIMARY KEY,
    customer_id     INT NOT NULL,
    request_type    VARCHAR(50) NOT NULL,
    status          ENUM('pending', 'processed') NOT NULL DEFAULT 'pending',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at    TIMESTAMP NULL DEFAULT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- Helpful indexes for search / sort operations
CREATE INDEX idx_customer_name ON customers(name);
CREATE INDEX idx_txn_customer ON transactions(customer_id);
CREATE INDEX idx_req_status ON requests(status);
