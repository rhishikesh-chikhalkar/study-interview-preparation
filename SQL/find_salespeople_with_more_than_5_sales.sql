-- Problem Statement:
-- Find all salespeople who made more than 5 sales.
-- Show their name and total sales count, sorted by count descending.
--
-- Why the junior dev's query failed:
-- SQL queries execute in a specific logical order, which is different from how they are written:
--   1. FROM (and JOINs) - Tables are resolved
--   2. WHERE - Row-level filtering (cannot use aggregates like COUNT(*) or aliases defined in SELECT)
--   3. GROUP BY - Rows are grouped
--   4. HAVING - Group-level/Aggregate filtering (runs after GROUP BY, allows using aggregates like COUNT(*))
--   5. SELECT - Columns are projected, aliases (like total_sales) are assigned
--   6. ORDER BY - Sorting is applied (can use SELECT aliases since it runs last)
--
-- Solution 1: Using HAVING (Recommended/Standard Approach)
SELECT
    rep_name,
    COUNT(*) AS total_sales
FROM
    interview_prep.sales_table
GROUP BY
    rep_name
HAVING
    COUNT(*) > 5
ORDER BY
    total_sales DESC;

-- Solution 2: Using a Subquery (Alternative Approach)
-- This works because the inner query completes its grouping and projection (where the 'total_sales' alias is defined)
-- before the outer query's WHERE clause filters the results.
SELECT
    rep_name,
    total_sales
FROM
    (
        SELECT
            rep_name,
            COUNT(*) AS total_sales
        FROM
            interview_prep.sales_table
        GROUP BY
            rep_name
    ) AS derived
WHERE
    total_sales > 5
ORDER BY
    total_sales DESC;

-- Solution 3: Using a Common Table Expression (CTE)
-- Similar to the subquery approach, but much cleaner and easier to read/maintain.
WITH rep_sales AS (
    SELECT
        rep_name,
        COUNT(*) AS total_sales
    FROM
        interview_prep.sales_table
    GROUP BY
        rep_name
)
SELECT
    rep_name,
    total_sales
FROM
    rep_sales
WHERE
    total_sales > 5
ORDER BY
    total_sales DESC;

-- Solution 4: Using Window Functions (No GROUP BY)
-- This calculates the count over partition rep_name on every record, then filters unique values.
-- (Note: Less efficient than Solution 1 due to row-level processing, but shows window function usage)
SELECT DISTINCT
    rep_name,
    total_sales
FROM
    (
        SELECT
            rep_name,
            COUNT(*) OVER (PARTITION BY rep_name) AS total_sales
        FROM
            interview_prep.sales_table
    ) AS windowed
WHERE
    total_sales > 5
ORDER BY
    total_sales DESC;


