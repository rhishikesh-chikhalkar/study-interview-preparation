-- Problem Statement:
-- Find employees earning the second highest salary in each department
--
-- Tables:
--   - employee_table (id, name, salary, dept_id)
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
            ROW_NUMBER() OVER (
                PARTITION BY
                    e.dept_id
                ORDER BY
                    e.employee_salary DESC
            ) as salary_rank
        FROM
            employee_table e
            INNER JOIN dept_table d ON e.dept_id = d.dept_id
    ) ranked
WHERE
    salary_rank = 2
ORDER BY
    dept_name,
    employee_salary DESC;