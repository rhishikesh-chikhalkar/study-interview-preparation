-- Create the employee table to store employee information and their department associations
CREATE TABLE IF NOT EXISTS
    interview_prep.employee_table (
        employee_id SERIAL PRIMARY KEY, -- Unique auto-incrementing identifier for each employee
        employee_name VARCHAR(50),      -- Employee's name
        employee_salary INT,            -- Employee's salary
        dept_id INT REFERENCES interview_prep.dept_table(dept_id) -- Foreign key referencing dept_table(dept_id)
    );

-- Seed the employee table with sample data across multiple departments
-- This allows testing of queries like finding Nth highest salaries per department
TRUNCATE TABLE interview_prep.employee_table RESTART IDENTITY;

INSERT INTO interview_prep.employee_table
    (employee_id, employee_name, employee_salary, dept_id)
VALUES
    -- Engineering
    (1, 'Rahul Sharma', 120000, 1),
    (2, 'Priya Patel', 110000, 1),
    (3, 'Amit Verma', 100000, 1),
    (4, 'Sneha Joshi', 95000, 1),
    (5, 'Vikas Kulkarni', 90000, 1),

    -- Finance
    (6, 'Neha Gupta', 105000, 2),
    (7, 'Rohan Mehta', 98000, 2),
    (8, 'Anjali Singh', 92000, 2),
    (9, 'Karan Shah', 87000, 2),
    (10, 'Pooja Desai', 83000, 2),

    -- Human Resources
    (11, 'Meera Nair', 85000, 3),
    (12, 'Sanjay Rao', 80000, 3),
    (13, 'Nikita Jain', 76000, 3),
    (14, 'Arjun Kapoor', 72000, 3),
    (15, 'Divya Menon', 68000, 3),

    -- Marketing
    (16, 'Akash Yadav', 95000, 4),
    (17, 'Ritika Sharma', 90000, 4),
    (18, 'Harsh Agarwal', 85000, 4),
    (19, 'Simran Kaur', 80000, 4),
    (20, 'Abhishek Roy', 75000, 4),

    -- Sales
    (21, 'Vivek Mishra', 130000, 5),
    (22, 'Shweta Bansal', 120000, 5),
    (23, 'Deepak Soni', 110000, 5),
    (24, 'Komal Patil', 100000, 5),
    (25, 'Manish Gupta', 95000, 5),

    -- Operations
    (26, 'Gaurav Saxena', 90000, 6),
    (27, 'Isha Kulkarni', 85000, 6),
    (28, 'Nitin Chavan', 80000, 6),
    (29, 'Bhavna Reddy', 76000, 6),
    (30, 'Saurabh Jain', 72000, 6),

    -- Product
    (31, 'Aditya Bansal', 140000, 7),
    (32, 'Kritika Arora', 130000, 7),
    (33, 'Yash Malhotra', 120000, 7),
    (34, 'Tanvi Goyal', 110000, 7),
    (35, 'Mohit Khanna', 100000, 7),

    -- Customer Support
    (36, 'Ayesha Khan', 70000, 8),
    (37, 'Rakesh Kumar', 67000, 8),
    (38, 'Saloni Joshi', 64000, 8),
    (39, 'Tarun Bhatia', 61000, 8),
    (40, 'Payal Sharma', 58000, 8),

    -- Legal
    (41, 'Naveen Iyer', 125000, 9),
    (42, 'Shruti Deshmukh', 118000, 9),
    (43, 'Ankit Tiwari', 112000, 9),
    (44, 'Madhuri Patil', 108000, 9),
    (45, 'Rohit Kulkarni', 102000, 9),

    -- IT
    (46, 'Siddharth Joshi', 115000, 10),
    (47, 'Pallavi Shah', 108000, 10),
    (48, 'Varun Gupta', 101000, 10),
    (49, 'Keerti Rao', 97000, 10),
    (50, 'Hemant Yadav', 93000, 10);