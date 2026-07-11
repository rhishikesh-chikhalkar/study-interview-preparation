-- Create the department table to store department metadata
CREATE TABLE IF NOT EXISTS
interview_prep.dept_table (
    -- Unique auto-incrementing identifier for each department
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(50)       -- Name of the department
);

-- Seed the department table with sample data for testing and prep
TRUNCATE TABLE interview_prep.dept_table RESTART IDENTITY CASCADE;

INSERT INTO interview_prep.dept_table
(dept_id, dept_name)
VALUES
(1, 'Engineering'),
(2, 'Finance'),
(3, 'Human Resources'),
(4, 'Marketing'),
(5, 'Sales'),
(6, 'Operations'),
(7, 'Product'),
(8, 'Customer Support'),
(9, 'Legal'),
(10, 'IT');
