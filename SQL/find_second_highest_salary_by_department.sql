-- Find employees earning the second highest salary in each department.
-- Uses DENSE_RANK() instead of ROW_NUMBER() or RANK() to handle ties properly:
--
-- Suppose salaries in a department are: [120k, 120k, 100k, 90k]
--   - ROW_NUMBER(): [1, 2, 3, 4] -> Rank 2 is 120k (duplicate of highest)
--   - RANK():       [1, 1, 3, 4] -> Rank 2 is skipped (returns nothing for rank 2)
--   - DENSE_RANK(): [1, 1, 2, 3] -> Rank 2 is 100k (correct second highest)
--
-- Tables:
--   - employee_table (employee_id, employee_name, employee_salary, dept_id)
--   - dept_table (dept_id, dept_name)
--
-- Output: employee_salary, employee_name, dept_name
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
            ) as salary_rank
        FROM
            interview_prep.employee_table e
            INNER JOIN interview_prep.dept_table d 
            ON e.dept_id = d.dept_id
    ) ranked
WHERE
    salary_rank = 2
ORDER BY
    dept_name,
    employee_salary DESC;