-- Create the sales table to store individual sales transactions
CREATE TABLE IF NOT EXISTS
interview_prep.sales_table (
    sale_id SERIAL PRIMARY KEY,    -- Unique transaction ID
    rep_name VARCHAR(50),          -- Name of the sales representative
    sale_amount DECIMAL(10, 2),    -- The value of the sale
    sale_date DATE                 -- The date the sale occurred
);

-- Seed the sales table with sample data ensuring some representatives have
-- > 5 sales
TRUNCATE TABLE interview_prep.sales_table RESTART IDENTITY;

INSERT INTO interview_prep.sales_table
(rep_name, sale_amount, sale_date)
VALUES
-- Alice (6 sales)
('Alice', 1500.00, '2026-06-01'),
('Alice', 2000.00, '2026-06-02'),
('Alice', 800.00, '2026-06-03'),
('Alice', 1200.00, '2026-06-04'),
('Alice', 3000.00, '2026-06-05'),
('Alice', 950.00, '2026-06-06'),

-- Bob (4 sales)
('Bob', 450.00, '2026-06-01'),
('Bob', 3200.00, '2026-06-03'),
('Bob', 1100.00, '2026-06-04'),
('Bob', 900.00, '2026-06-05'),

-- Charlie (7 sales)
('Charlie', 2500.00, '2026-06-01'),
('Charlie', 500.00, '2026-06-02'),
('Charlie', 1750.00, '2026-06-02'),
('Charlie', 990.00, '2026-06-03'),
('Charlie', 120.00, '2026-06-04'),
('Charlie', 3100.00, '2026-06-05'),
('Charlie', 850.00, '2026-06-06'),

-- David (2 sales)
('David', 5000.00, '2026-06-02'),
('David', 150.00, '2026-06-05'),

-- Eve (8 sales)
('Eve', 750.00, '2026-06-01'),
('Eve', 950.00, '2026-06-02'),
('Eve', 1200.00, '2026-06-03'),
('Eve', 300.00, '2026-06-04'),
('Eve', 2200.00, '2026-06-05'),
('Eve', 1800.00, '2026-06-05'),
('Eve', 900.00, '2026-06-06'),
('Eve', 1500.00, '2026-06-07');
