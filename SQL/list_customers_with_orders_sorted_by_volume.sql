-- sameer.mahabole@onixnet.com
--
-- Write a SQL query to list all customers alongside their individual orders.
--
-- The query must meet the following conditions:
--   1. Include Everyone: Show every customer in the database, even if they
--      have never placed an order.
--   2. Keep Rows Granular: Do not collapse the rows. Every single individual
--      order must be visible as a separate row in the final output.
--   3. Sort by Volume: Sort the entire result set so that the customers with
--      the highest total order count appear first. If a customer has 0 orders,
--      they should appear at the bottom.
--
-- Schema:
--   customers(customer_id, customer_name)
--   orders(order_id, customer_id, order_date, order_amount)
--

SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.order_date,
    o.order_amount
FROM
    interview_prep.customers AS c
LEFT JOIN
    interview_prep.orders AS o
    ON c.customer_id = o.customer_id
ORDER BY
    COUNT(o.order_id) OVER (
        PARTITION BY
            c.customer_id
    ) DESC,
    c.customer_id,
    o.order_id ASC;
