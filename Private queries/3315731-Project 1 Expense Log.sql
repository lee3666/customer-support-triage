CREATE TABLE expenses (
    expense_id   INT PRIMARY KEY,
    expense_date DATE NOT NULL,
    category     VARCHAR(30) NOT NULL,
    description  VARCHAR(100),
    amount       DECIMAL(10, 2) NOT NULL
);

INSERT INTO expenses (expense_id, expense_date, category, description, amount) VALUES
(1,  '2024-10-01', 'Groceries',   'Weekly shop',              82.40),
(2,  '2024-10-02', 'Transport',   'Bus pass',                 45.00),
(3,  '2024-10-03', 'Dining',      'Lunch with colleagues',    28.75),
(4,  '2024-10-05', 'Groceries',   'Weekly shop',              91.10),
(5,  '2024-10-07', 'Utilities',   'Electricity bill',        120.00),
(6,  '2024-10-09', 'Entertainment','Cinema tickets',           24.00),
(7,  '2024-10-11', 'Groceries',   'Weekly shop',              78.60),
(8,  '2024-10-14', 'Dining',      'Dinner out',               62.30),
(9,  '2024-10-15', 'Transport',   'Fuel',                     55.20),
(10, '2024-10-18', 'Groceries',   'Weekly shop',              88.90),
(11, '2024-10-20', 'Utilities',   'Internet bill',            60.00),
(12, '2024-10-22', 'Entertainment','Concert',                 85.00),
(13, '2024-10-25', 'Groceries',   'Weekly shop',              95.40),
(14, '2024-10-28', 'Dining',      'Takeaway',                 22.50),
(15, '2024-10-30', 'Transport',   'Bus pass',                 45.00),
(16, '2024-11-01', 'Groceries',   'Weekly shop',              84.20),
(17, '2024-11-03', 'Utilities',   'Electricity bill',        135.50),
(18, '2024-11-05', 'Dining',      'Birthday dinner',         110.00),
(19, '2024-11-07', 'Groceries',   'Weekly shop',              79.30),
(20, '2024-11-10', 'Transport',   'Fuel',                     58.80),
(21, '2024-11-12', 'Entertainment','Streaming subscription',  15.99),
(22, '2024-11-14', 'Groceries',   'Weekly shop',              92.10),
(23, '2024-11-17', 'Dining',      'Lunch',                    18.40),
(24, '2024-11-20', 'Utilities',   'Internet bill',            60.00),
(25, '2024-11-22', 'Groceries',   'Weekly shop',              86.70),
(26, '2024-11-25', 'Transport',   'Bus pass',                 45.00),
(27, '2024-11-28', 'Entertainment','Cinema tickets',           26.00),
(28, '2024-11-30', 'Groceries',   'Weekly shop',             101.20),
(29, '2024-12-02', 'Utilities',   'Electricity bill',        148.90),
(30, '2024-12-04', 'Dining',      'Holiday dinner',          145.00),
(31, '2024-12-06', 'Groceries',   'Weekly shop',              97.50),
(32, '2024-12-09', 'Entertainment','Gifts',                  220.00),
(33, '2024-12-11', 'Transport',   'Fuel',                     62.40),
(34, '2024-12-13', 'Groceries',   'Weekly shop',             105.80),
(35, '2024-12-15', 'Dining',      'Lunch with friends',       48.20),
(36, '2024-12-18', 'Utilities',   'Internet bill',            60.00),
(37, '2024-12-20', 'Groceries',   'Weekly shop',             112.30),
(38, '2024-12-22', 'Entertainment','Holiday party',           75.00),
(39, '2024-12-26', 'Transport',   'Bus pass',                 45.00),
(40, '2024-12-29', 'Groceries',   'Weekly shop',             118.60);


SELECT COUNT(*) FROM expenses;

SELECT *
FROM expenses
WHERE expense_date >= '2024-12-01'
    AND expense_date < '2025-01-01'
ORDER BY expense_date DESC;


SELECT SUM(amount) AS total_spend
FROM expenses;

SELECT ROUND(AVG(amount), 2) AS avg_amount
FROM expenses;

SELECT category, COUNT(*) AS num_expenses
FROM expenses
GROUP BY category
ORDER BY num_expenses DESC;

SELECT category, SUM(amount) AS total_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC;

SELECT
    YEAR(expense_date)  AS yr,
    MONTH(expense_date) AS mo,
    SUM(amount)         AS total_spent
FROM expenses
GROUP BY YEAR(expense_date), MONTH(expense_date)
ORDER BY yr, mo;

SELECT
    DATE_FORMAT(expense_date, '%Y-%m') AS month,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY DATE_FORMAT(expense_date, '%Y-%m')
ORDER BY month;







SELECT *
FROM expenses
ORDER BY amount DESC
LIMIT 1;


SELECT 
    expense_id,
    description,
    amount,
    CASE
        WHEN amount >= 100 THEN 'Large'
        ELSE 'Normal'
    END AS size_label
FROM expenses
ORDER BY amount DESC;


SELECT SUM(amount) AS q4_groceries
FROM expenses
WHERE category = 'Groceries'
    AND expense_date >= '2024-10-01'
    AND expense_date < '2025-01-01';


SELECT SUM(amount) AS nov_dining
FROM expenses
WHERE category = 'Dining'
    AND expense_date >= '2024-11-01'
    AND expense_date < '2024-12-01';