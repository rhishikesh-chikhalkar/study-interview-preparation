"""
Problem Statement:
Find employees earning the second highest salary in each department.

Tables:
  - employee_table: id, name, salary, dept_id
  - dept_table: dept_id, dept_name

Output: employee_salary, employee_name, dept_name
"""

import pandas as pd

# Example data
employees = [
    {"id": 1, "name": "Alice", "salary": 60000, "dept_id": 1},
    {"id": 2, "name": "Bob", "salary": 70000, "dept_id": 1},
    {"id": 3, "name": "Charlie", "salary": 80000, "dept_id": 1},
    {"id": 4, "name": "Diana", "salary": 55000, "dept_id": 2},
    {"id": 5, "name": "Eve", "salary": 75000, "dept_id": 2},
    {"id": 6, "name": "Frank", "salary": 65000, "dept_id": 2},
]

departments = [
    {"dept_id": 1, "dept_name": "Engineering"},
    {"dept_id": 2, "dept_name": "Sales"},
]

# Create DataFrames
df_emp = pd.DataFrame(employees)
df_dept = pd.DataFrame(departments)

# Merge tables
df_merged = df_emp.merge(df_dept, on="dept_id")

# Get second highest salary in each department
result = df_merged.loc[
    df_merged.groupby("dept_id")["salary"].rank(method="dense", ascending=False) == 2
]
result = result[["salary", "name", "dept_name"]]
result = result.rename(columns={"salary": "employee_salary", "name": "employee_name"})

print(result)
print("\nSecond Highest Salary Earners by Department:")
print(result.to_string(index=False))
