-- Find employees earning the second highest salary in each department.
-- Uses DENSE_RANK() instead of ROW_NUMBER() or RANK() to handle ties properly:
--
-- Suppose salaries in a department are: [120k, 120k, 100k, 90k]
--   - ROW_NUMBER(): [1, 2, 3, 4] -> Rank 2 is 120k (duplicate of highest)
--   - RANK():       [1, 1, 3, 4] -> Rank 2 is skipped (returns nothing
--                   for rank 2)
--   - DENSE_RANK(): [1, 1, 2, 3] -> Rank 2 is 100k (correct second highest)
--
-- Tables:
--   - employee_table (employee_id, employee_name, employee_salary, dept_id)
--   - dept_table (dept_id, dept_name)
--
-- Output: employee_salary, employee_name, dept_name
-- Solution 1: Subquery with DENSE_RANK() (Recommended/Standard Approach)
SELECT
    employee_salary,
    employee_name,
    dept_name
FROM
    (
        SELECT
            e.employee_salary,
            e.employee_name,
            d.dept_name,
            DENSE_RANK() OVER (
                PARTITION BY
                    e.dept_id
                ORDER BY
                    e.employee_salary DESC
            ) AS salary_rank
        FROM
            interview_prep.employee_table AS e
        INNER JOIN interview_prep.dept_table AS d
            ON e.dept_id = d.dept_id
    ) AS ranked
WHERE
    salary_rank = 2
ORDER BY
    dept_name ASC,
    employee_salary DESC;

-- Solution 2: CTE with DENSE_RANK() (Clean & Readable Window Function Approach)
WITH ranked_employees AS (
    SELECT
        e.employee_salary,
        e.employee_name,
        d.dept_name,
        DENSE_RANK() OVER (
            PARTITION BY e.dept_id
            ORDER BY e.employee_salary DESC
        ) AS salary_rank
    FROM
        interview_prep.employee_table AS e
    INNER JOIN interview_prep.dept_table AS d ON e.dept_id = d.dept_id
)

SELECT
    employee_salary,
    employee_name,
    dept_name
FROM
    ranked_employees
WHERE
    salary_rank = 2
ORDER BY
    dept_name ASC,
    employee_salary DESC;

-- Solution 3: Correlated Subquery (Classic approach - No Window Functions
--             required)
-- Find employees where there is exactly 1 distinct salary higher than theirs
-- in the same department.
SELECT
    e1.employee_salary,
    e1.employee_name,
    d.dept_name
FROM
    interview_prep.employee_table AS e1
INNER JOIN interview_prep.dept_table AS d ON e1.dept_id = d.dept_id
WHERE
    1 = (
        SELECT COUNT(DISTINCT e2.employee_salary)
        FROM interview_prep.employee_table AS e2
        WHERE
            e2.dept_id = e1.dept_id
            AND e2.employee_salary > e1.employee_salary
    )
ORDER BY
    d.dept_name ASC,
    e1.employee_salary DESC;
