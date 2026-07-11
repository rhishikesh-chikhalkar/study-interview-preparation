-- For each product category, find the top 2 products by total revenue in the 
-- current year. Return: category, product_name, revenue, rank.
--
-- Schema:
--   products(product_id, name, category)
--   sales(sale_id, product_id, revenue, sale_date)
--

-- Solution 1: CTE with RANK() (Standard Window Function Approach)
WITH
product_revenue_ranks AS (
    SELECT
        prod.category,
        prod.name          AS product_name,
        SUM(sales.revenue) AS total_revenue,
        RANK() OVER (
            PARTITION BY
                prod.category
            ORDER BY
                SUM(sales.revenue) DESC
        )                  AS revenue_rank
    FROM
        interview_prep.products AS prod
    INNER JOIN interview_prep.sales AS sales
        ON prod.product_id = sales.product_id
    WHERE
        EXTRACT(
            YEAR
            FROM
            sales.sale_date
        ) = EXTRACT(
            YEAR
            FROM
            CURRENT_DATE
        )
    GROUP BY
        prod.category,
        prod.name
)

SELECT
    category,
    product_name,
    total_revenue,
    revenue_rank
FROM
    product_revenue_ranks
WHERE
    revenue_rank <= 2
ORDER BY
    category ASC,
    revenue_rank ASC;

-- Solution 2: Subquery with DENSE_RANK() (Handles duplicate ranking
-- differences)
SELECT
    category,
    product_name,
    revenue,
    rnk
FROM
    (
        SELECT
            p.category,
            p.name         AS product_name,
            SUM(s.revenue) AS revenue,
            DENSE_RANK() OVER (
                PARTITION BY
                    p.category
                ORDER BY
                    SUM(s.revenue) DESC
            )              AS rnk
        FROM
            interview_prep.products AS p
        INNER JOIN interview_prep.sales AS s ON p.product_id = s.product_id
        WHERE
            EXTRACT(
                YEAR
                FROM
                s.sale_date
            ) = EXTRACT(
                YEAR
                FROM
                CURRENT_DATE
            )
        GROUP BY
            p.category,
            p.name
    ) AS ranked
WHERE
    rnk <= 2
ORDER BY
    category,
    rnk;
