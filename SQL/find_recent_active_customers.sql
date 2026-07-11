-- Find customers who have placed more than 3 orders in the last 30 days, 
-- along with their total spend. Sort by total spend descending.
--
-- Schema:
--   customers(customer_id, name, country)
--   orders(order_id, customer_id, amount, created_at)
--

-- Solution 1: Group By & Having (Most efficient for simple lookups)
SELECT
    cust.customer_id,
    cust.name           AS customer_name,
    SUM(ord.amount)     AS total_spends,
    COUNT(ord.order_id) AS order_count
FROM
    interview_prep.customers AS cust
INNER JOIN interview_prep.orders AS ord
    ON cust.customer_id = ord.customer_id
WHERE
    ord.created_at >= NOW() - INTERVAL '30 days'
GROUP BY
    cust.customer_id,
    cust.name
HAVING
    COUNT(ord.order_id) > 3
ORDER BY
    total_spends DESC;

-- Solution 2: CTE Approach (Clean separation of aggregation and attributes)
WITH
customer_order_aggregates AS (
    SELECT
        customer_id,
        COUNT(order_id) AS order_count,
        SUM(amount)     AS total_spends
    FROM
        interview_prep.orders
    WHERE
        created_at >= NOW() - INTERVAL '30 days'
    GROUP BY
        customer_id
    HAVING
        COUNT(order_id) > 3
)

SELECT
    cust.customer_id,
    cust.name AS customer_name,
    agg.order_count,
    agg.total_spends
FROM
    interview_prep.customers AS cust
INNER JOIN customer_order_aggregates AS agg
    ON cust.customer_id = agg.customer_id
ORDER BY
    agg.total_spends DESC;

-- Solution 3: Window Functions (Alternative representation)
WITH
partition_stats AS (
    SELECT
        customer_id,
        amount,
        COUNT(order_id) OVER (
            PARTITION BY
                customer_id
        ) AS order_count,
        SUM(amount) OVER (
            PARTITION BY
                customer_id
        ) AS total_amount
    FROM
        interview_prep.orders
    WHERE
        created_at >= NOW() - INTERVAL '30 days'
),

filtered_stats AS (
    SELECT DISTINCT
        customer_id,
        order_count,
        total_amount
    FROM
        partition_stats
    WHERE
        order_count > 3
)

SELECT
    cust.customer_id,
    cust.name          AS customer_name,
    stats.order_count,
    stats.total_amount AS total_spends
FROM
    interview_prep.customers AS cust
INNER JOIN filtered_stats AS stats
    ON cust.customer_id = stats.customer_id
ORDER BY
    stats.total_amount DESC;
