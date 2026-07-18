---

- **057. Why is NumPy faster than lists? What is Vectorization, and how do you handle missing data in Pandas DataFrames?**
  **1. Memory Locality (NumPy vs. Lists)**
  A standard Python list is an array of memory pointers. If you have a list of 1,000 integers, the list holds 1,000 pointers, each pointing to a separate `int` object scattered randomly across your RAM. Navigating this fragmented memory is incredibly slow.
  NumPy arrays are built in C. They allocate a single, continuous block of memory holding raw C-types (like 32-bit integers). The CPU can read a NumPy array instantly because it simply scans a single continuous memory block.
  **2. Vectorization & SIMD**
  Vectorization is the process of applying a mathematical operation to an entire array at once, rather than looping through it element by element.
  - **The Architecture:** Under the hood, NumPy utilizes your CPU's **SIMD** (Single Instruction, Multiple Data) architecture. It allows the CPU processor to add 4, 8, or 16 numbers together in a single clock cycle, completely bypassing Python's slow bytecode execution.
  **3. Handling Missing Data (Pandas)**
  When dealing with missing data (`NaN`) in a DataFrame, a senior engineer doesn't just loop through and replace them. They use optimized Pandas methods:
  - **Imputation:** `df.fillna(df.mean())` to replace missing values with the column's statistical mean.
  - **Forward/Backward Filling:** `df.ffill()` propagates the last valid observation forward (critical for time-series data).
  - **Dropping:** `df.dropna(subset=['critical_column'])` to drop rows only if the most important data is missing.
  **The Code Example:**
  ```python
  import numpy as np

  # BAD: The Python Loop (Slow, scalar math)
  python_list = list(range(1000000))
  squared_list = [x ** 2 for x in python_list]

  # GOOD: Vectorization (SIMD, C-level speed)
  numpy_array = np.arange(1000000)
  # No loop! The entire array is squared simultaneously at the CPU level.
  squared_array = numpy_array ** 2
  ```

---

---

- **079. What advantage does the NumPy array have over a Nested List?**

NumPy arrays are more **efficient, faster, and memory-optimized** compared to Python’s nested lists.

### **Key Advantages:**

- **Faster computations**
- **Less memory usage**
- **Vectorized operations**
- **Built-in mathematical functions**
- **Multidimensional support**

### **Example:**

```python
import numpy as np

# Creating a NumPy array
arr = np.array([[1, 2], [3, 4]])

# Performing vectorized operations
arr_squared = arr ** 2
print(arr_squared)  # Output: [[ 1  4] [ 9 16]]

```

---

---

- **102. What is a NumPy array?**

A **NumPy array** is a powerful, grid-like data structure provided by the [NumPy](https://chatgpt.com/?q=NumPy) library in Python. It is optimized for numerical computations and supports:

- **Fast processing** compared to Python lists.
- **Memory efficiency** (stores elements of the same type).
- **Vectorized operations** (avoids explicit loops).

### **Example:**

```python
python
CopyEdit
import numpy as np

# Creating a 1D NumPy array
arr = np.array([1, 2, 3, 4])
print(arr)  # Output: [1 2 3 4]

```

---

### **Why use NumPy instead of lists?**

| Feature     | Python List                    | NumPy Array                    |
| ----------- | ------------------------------ | ------------------------------ |
| Storage     | Stores mixed data types        | Stores homogeneous data types  |
| Performance | Slower (due to dynamic typing) | Faster (fixed type, optimized) |
| Operations  | Requires explicit loops        | Supports vectorized operations |

### **Vectorized Operations Example:**

```python
python
CopyEdit
arr = np.array([1, 2, 3, 4])
print(arr * 2)  # Output: [2 4 6 8] (multiplies each element)

```

Unlike lists, NumPy performs element-wise operations efficiently.

---

**30. What is the difference between Matrices and Arrays?**

| Feature    | Matrices                                                                            | Arrays                                                                                                |
| ---------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Definition | A matrix comes from linear algebra and is a two-dimensional representation of data. | An array is a sequence of objects of similar data type. An array within another array forms a matrix. |
| Operations | Comes with a powerful set of mathematical operations for data manipulation.         | Supports element-wise operations and can be multi-dimensional.                                        |

---

**31. How do you get indices of n maximum values in a NumPy array?**

To get the n maximum values' indices in a NumPy array, use `np.argsort()`, which returns the indices that would sort the array, then slice the last n values.

```
import numpy as np
arr = np.array([1, 3, 2, 7, 5])
n = 2  # Number of maximum values
# Get indices of n maximum values
indices = np.argsort(arr)[-n:]
print(indices)  # Output: [4, 3], indices of the two largest values (5, 7)
```

This returns the indices of the largest values in ascending order.

---

**32. How would you obtain the `res_set` from the `train_set` and the `test_set`?**

To split a dataset into `train_set` and `test_set`, use scikit-learn's `train_test_split()` function, which randomly divides the dataset into training and testing subsets.

```
from sklearn.model_selection import train_test_split
# Assuming res_set is your dataset
res_set = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Split res_set into 80% train_set and 20% test_set
train_set, test_set = train_test_split(res_set, test_size=0.2, random_state=42)
print("Train Set:", train_set)
print("Test Set:", test_set)
```

Here, 80% of the data is in `train_set`, and 20% is in `test_set`. You can adjust `test_size` for different splits.

---

**33. How would you import a decision tree classifier in sklearn? Choose the correct option.**

1. `from sklearn.decision_tree import DecisionTreeClassifier`
2. `from sklearn.ensemble import DecisionTreeClassifier`
3. `from sklearn.tree import DecisionTreeClassifier`
4. None of these

**Answer:** 3. `from sklearn.tree import DecisionTreeClassifier`

---

**34. How to access a publicly shared Google Spreadsheet in Python?**

1. Ensure the file is publicly accessible: Click on "Share" in Google Sheets and set it to "Anyone with the link can view."
2. Replace `/edit` in the URL with `/export?format=csv`.

Example: `https://docs.google.com/spreadsheets/d/<your_sheet_id>/export?format=csv`

1. Access the CSV data in Python:

```
import pandas as pd
# URL of the Google Spreadsheet in CSV format
url = "https://docs.google.com/spreadsheets/d/<your_sheet_id>/export?format=csv"
# Load the dataset into a pandas DataFrame
df = pd.read_csv(url)
# Print the DataFrame
print(df)
```

This reads the CSV file directly from Google Spreadsheet into a Pandas DataFrame for further processing.

---

**35. What is the difference between the two data series given below?**

Given:

```
df['Name']
df.loc[:, 'Name']
```

Where:

```
df = pd.DataFrame({'Name': ['aa', 'bb', 'xx', 'uu'], 'Age': [21, 16, 50, 33]})
```

**Options:**

1. The first is a view of the original DataFrame, and the second is a copy.
2. The second is a view of the original DataFrame, and the first is a copy.
3. Both are copies of the original DataFrame.
4. Both are views of the original DataFrame.

**Answer:** 3. Both are copies of the original DataFrame.

---

**36. How to fix the error "temp.csv" while reading a file using pandas?**

**Error:**

```
Traceback (most recent call last):
File "<input>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode character.
```

**Options:**

1. `pd.read_csv("temp.csv", compression='gzip')`
2. `pd.read_csv("temp.csv", dialect='str')`
3. `pd.read_csv("temp.csv", encoding='utf-8')`
4. None of these

**Answer:** 3. `pd.read_csv("temp.csv", encoding='utf-8')`

This error occurs due to a difference between UTF-8 encoding and Unicode. Specifying `encoding='utf-8'` resolves it.

---

**37. How do you set a line width in the plot given below?**

**Matplotlib Example:**

```
import matplotlib.pyplot as plt
plt.plot([1,2,3,4], lw=3)  # Correct option
plt.show()
```

**Answer:** In line two, write `plt.plot([1,2,3,4], lw=3)`.

---

**38. How would you reset the index of a DataFrame to a given list?**

**Answer:**

```
df.reindex_like(new_index,)  # Correct option
```

---

**39. What is the difference between `range()` and `xrange()` functions in Python?**

- In Python 2:
  - `range()`: Returns a list, storing all values in memory.
  - `xrange()`: Returns an iterator, generating numbers lazily.
- In Python 3:
  - `xrange()` was removed.
  - `range()` behaves like `xrange()`, generating numbers lazily.

---

**40. How can you check whether a pandas DataFrame is empty or not?**

**Example:**

```
import pandas as pd
# Create an empty DataFrame
df = pd.DataFrame()
# Check if the DataFrame is empty
if df.empty:
    print("The DataFrame is empty.")
else:
    print("The DataFrame is not empty.")
```

---

**41. Write a code to sort an array in NumPy by the (N-1)th column.**

**Example:**

```
import numpy as np
# Sample 2D array
arr = np.array([[1, 5, 3],
                [4, 2, 9],
                [7, 8, 6]])
# Sort the array by the last (N-1) column
sorted_arr = arr[arr[:, -1].argsort()]
print(sorted_arr)
```

---

**42. How do you create a Series from a list, NumPy array, and dictionary?**

1. **From a List:**

```
import pandas as pd
my_list = [1, 2, 3, 4]
series_from_list = pd.Series(my_list)
print(series_from_list)
```

1. **From a NumPy Array:**

```
import numpy as np
my_array = np.array([10, 20, 30, 40])
series_from_array = pd.Series(my_array)
print(series_from_array)
```

1. **From a Dictionary:**

```
my_dict = {'a': 1, 'b': 2, 'c': 3}
series_from_dict = pd.Series(my_dict)
print(series_from_dict)
```

---

**43. How do you get the items not common to both Series A and Series B?**

**Using `symmetric_difference()`:**

```
import pandas as pd
A = pd.Series([1, 2, 3, 4, 5])
B = pd.Series([4, 5, 6, 7, 8])
# Get the items not common to both Series
result = pd.Series(list(set(A).symmetric_difference(set(B))))
print(result)
```

**Using `~isin()` and `append()`:**

```
# Items not in both A and B
result = A[~A.isin(B)].append(B[~B.isin(A)])
print(result)
```

---

---

- **103. How do you keep only the top two most frequent values as it is and replace everything else as ‘other’ in a series?**

### Input:

```python
python
CopyEdit
import pandas as pd
import numpy as np

np.random.seed(100)
ser = pd.Series(np.random.randint(1, 5, [12]))

```

### Solution:

```python
python
CopyEdit
print("Top 2 Freq:", ser.value_counts())
ser[~ser.isin(ser.value_counts().index[:2])] = 'Other'
ser

```

---

---

- **104. How do you find the positions of numbers that are multiples of three from a series?**

### Input:

```python
python
CopyEdit
import pandas as pd
import numpy as np

ser = pd.Series(np.random.randint(1, 10, 7))
ser

```

### Solution:

```python
python
CopyEdit
print(ser)
np.argwhere(ser % 3 == 0)

```

---

---

- **105. How do you compute the Euclidean distance between two series?**

### Input:

```python
python
CopyEdit
import pandas as pd
import numpy as np

p = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
q = pd.Series([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])

```

### Solution:

```python
python
CopyEdit
sum((p - q)**2)**.5

```

### Solution using function:

```python
python
CopyEdit
np.linalg.norm(p - q)

```

> You can see that the Euclidean distance can be calculated using two ways.

---

---

- **106. How do you reverse the rows of a DataFrame?**

### Input:

```python
python
CopyEdit
import pandas as pd
import numpy as np

df = pd.DataFrame(np.arange(25).reshape(5, -1))

```

### Solution:

```python
python
CopyEdit
df.iloc[::-1, :]

```

---

---

- **108. Which Python library is built on top of Matplotlib and Pandas to ease data plotting?**

Seaborn is a Python library built on top of Matplotlib and Pandas to ease data plotting. It is a data visualization library in Python that provides a high-level interface for drawing statistical informative graphs.

---

---

- **119. How do we combine dataframes in Pandas?**

The following are the ways through which dataframes in **Pandas** can be combined:

1. **Concatenating them by vertically stacking** the two dataframes.
2. **Concatenating them by horizontally stacking** the two dataframes.
3. **Putting them together in a single column.**

---

---

### 100. What are the benefits of NumPy arrays over (nested) Python lists?

- **Speed**: NumPy arrays are faster.
- **Memory Efficiency**: Uses less memory compared to lists.
- **Vectorized Operations**: Supports elementwise addition, multiplication, etc.
- **Built-in Functions**: Provides statistical, algebraic, and transformation functions.

```python
python
CopyEdit
import numpy as np
arr = np.array([1, 2, 3])
print(arr * 2)  # Output: [2 4 6]

```

---

---

- **143. What is the best way to add values to a Python array?**

To add elements to an array, the `append()`, `extend()`, and `insert(i, x)` methods can be used.

---

### 102. What is the best way to remove values from a Python array?

The `pop()` and `remove()` methods can remove elements from an array. The difference between these two functions is that one returns the removed value while the other does not.

---

### 107. What is a Pandas DataFrame?

A **DataFrame** is a 2D, mutable, and tabular data structure in Pandas that contains labeled rows and columns. It is widely used for data manipulation and analysis.

---

### 120. Write a Python program to generate the Fibonacci series.

```python
python
CopyEdit
# Enter the number of terms needed (e.g., 0,1,1,2,3,5....)
a = int(input("Enter the terms: "))
f, s = 0, 1

if a == 0:
    print("The requested series is", f)
else:
    print(f, s, end=" ")
    for x in range(2, a):
        next = f + s
        print(next, end=" ")
        f, s = s, next

```

**Output Example:**

```
yaml
CopyEdit
Enter the terms: 5
0 1 1 2 3

```

---

---

- **146. Can you write a sorting algorithm with a numerical dataset?**

```python
python
CopyEdit
nums = [5, 2, 9, 1, 5, 6]
nums.sort()
print(nums)

```

**Output:**

```
csharp
CopyEdit
[1, 2, 5, 5, 6, 9]

```

---

---

- **151. In NumPy, how do you read CSV data into an array?**

```python
python
CopyEdit
import numpy as np
data = np.genfromtxt('data.csv', delimiter=',')

```

---

---

- **172. What is the difference between Python Arrays and Lists?**

- **Arrays** in Python can only contain elements of the same data type (homogeneous). They consume less memory than lists.

---

- **196. How Do You Create a Class in Python?**

A class is created using the `class` keyword.

```python
python
CopyEdit
class InterviewbitEmployee:
   def __init__(self, emp_name):
       self.emp_name = emp_name

```

To create an object (instantiate a class):

```python
python
CopyEdit
emp_1 = InterviewbitEmployee("Mr. Employee")

```

To access the `emp_name` attribute:

```python
python
CopyEdit
print(emp_1.emp_name)  # Prints Mr. Employee

```

### Adding Methods to a Class

```python
python
CopyEdit
class InterviewbitEmployee:
   def __init__(self, emp_name):
       self.emp_name = emp_name

   def introduce(self):
       print("Hello, I am " + self.emp_name)

```

Here, `self` refers to the current instance of the class. It must be the first parameter in any class method.

To call the method:

```python
python
CopyEdit
emp_1.introduce()

```

### Complete Example

```python
python
CopyEdit
class InterviewbitEmployee:
   def __init__(self, emp_name):
       self.emp_name = emp_name

   def introduce(self):
       print("Hello, I am " + self.emp_name)

# Create an object of InterviewbitEmployee class
emp_1 = InterviewbitEmployee("Mr. Employee")
print(emp_1.emp_name)    # Print employee name
emp_1.introduce()        # Introduce the employee

```

This provides a structured explanation of inheritance and class creation in Python. Let me know if you need any modifications.

---

# **Python Pandas Interview Questions**

---

## **1. Can you get items of series A that are not available in another series B?**

This can be achieved using the `~` (not/negation symbol) and `isin()` method:

```python
python
CopyEdit
import pandas as pd
df1 = pd.Series([2, 4, 8, 10, 12])
df2 = pd.Series([8, 12, 10, 15, 16])
df1 = df1[~df1.isin(df2)]
print(df1)

```

**Output:**

```
go
CopyEdit
0    2
1    4
dtype: int64

```

---

---

- **197. Can Pandas recognize dates while importing data from different sources?**

Yes, but it requires additional configuration. The `parse_dates` argument helps convert date strings into `datetime` objects.

```python
python
CopyEdit
import pandas as pd
from datetime import datetime

dateparser = lambda date_val: datetime.strptime(date_val, '%Y-%m-%d %H:%M:%S')

df = pd.read_csv("some_file.csv", parse_dates=['datetime_column'], date_parser=dateparser)

```

---

---

- **198. How will you get the items that are not common to both given Series A and B?**

This can be achieved by finding the **union** of both series, then removing the **intersection**.

```python
python
CopyEdit
import pandas as pd
import numpy as np

df1 = pd.Series([2, 4, 5, 8, 10])
df2 = pd.Series([8, 10, 13, 15, 17])

p_union = pd.Series(np.union1d(df1, df2))  # Union of series
p_intersect = pd.Series(np.intersect1d(df1, df2))  # Intersection of series

unique_elements = p_union[~p_union.isin(p_intersect)]
print(unique_elements)

```

**Output:**

```
go
CopyEdit
0     2
1     4
2     5
5    13
6    15
7    17
dtype: int64

```

---

---

- **199. How will you delete indices, rows, and columns from a DataFrame?**

### **Deleting an Index**

You can remove the index name by:

```python
python
CopyEdit
df.index.name = None
# Or
del df.index.name

```

### **Deleting Rows/Columns**

Use `drop()` with the `axis` parameter:

- `axis=0` → Deletes a row
- `axis=1` → Deletes a column

```python
python
CopyEdit
df.drop('row_label', axis=0, inplace=True)  # Delete a row
df.drop('column_name', axis=1, inplace=True)  # Delete a column

```

### **Removing Duplicates**

```python
python
CopyEdit
df.drop_duplicates(inplace=True)

```

---

---

- **200. How to add a new column to a Pandas DataFrame?**

```python
python
CopyEdit
import pandas as pd

data_info = {
    'first': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
    'second': pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
}

df = pd.DataFrame(data_info)

# Add new column 'third'
df['third'] = pd.Series([10, 20, 30], index=['a', 'b', 'c'])

# Add new column 'fourth'
df['fourth'] = df['first'] + df['third']

print(df)

```

---

---

- **201. What is reindexing in Pandas?**

Reindexing adjusts a DataFrame to a new index, optionally filling missing values. If a value is missing, Pandas assigns `NaN`.

```python
python
CopyEdit
df = df.reindex(new_index)

```

It can also change the index of rows and columns dynamically.

---

---

- **202. How will you identify and handle missing values in a DataFrame?**

### **Identifying Missing Values**

```python
python
CopyEdit
missing_data_count = df.isnull().sum()

```

### **Handling Missing Values**

- Replace missing values with **0**
  ```python
  python
  CopyEdit
  df['column_name'].fillna(0, inplace=True)

  ```
- Replace missing values with the **mean**
  ```python
  python
  CopyEdit
  df['column_name'].fillna(df['column_name'].mean(), inplace=True)

  ```

---

---

- **203. Can you create a Pandas Series from a dictionary?**

Yes, a **Series** is a one-dimensional labeled array that can be created from a dictionary:

```python
python
CopyEdit
import pandas as pd

dict_info = {'key1': 2.0, 'key2': 3.1, 'key3': 2.2}

series_obj = pd.Series(dict_info)
print(series_obj)

```

**Output:**

```
go
CopyEdit
key1    2.0
key2    3.1
key3    2.2
dtype: float64

```

By default, keys are sorted in ascending order. If an index is specified, the index labels will be extracted from the dictionary.

---

---

- **204. How will you combine different Pandas DataFrames?**

### **Using `append()`**

Stacks DataFrames **horizontally**:

```python
python
CopyEdit
df1.append(df2)

```

### **Using `concat()`**

Stacks DataFrames **vertically** (when columns are the same):

```python
python
CopyEdit
pd.concat([df1, df2])

```

### **Using `join()`**

Combines DataFrames based on common columns:

```python
python
CopyEdit
df1.join(df2)

```

---

---

- **205. What is a Pandas DataFrame?**

A **DataFrame** is a **2D mutable** tabular structure with labeled axes (rows and columns).

### **Syntax to Create a DataFrame**

```python
python
CopyEdit
import pandas as pd

dataframe = pd.DataFrame(data, index, columns, dtype)

```

Where:

- **data** → Can be a `Series`, `dict`, `ndarray`, `lists`, etc.
- **index** → (Optional) Row labels
- **columns** → (Optional) Column labels
- **dtype** → (Optional) Data type of columns

---

---

- **206. What do you know about Pandas?**

- **Pandas** is an **open-source** Python library for data analysis and manipulation.
- The name **Pandas** is derived from **"Panel Data"**, representing multi-dimensional data.
- It was developed in **2008** by **Wes McKinney**.
- It is widely used in **data preprocessing, cleaning, transformation, and analysis**.

### **Major Steps of Data Analysis in Pandas**

1. **Load** data
2. **Clean/Manipulate** data
3. **Prepare** data
4. **Model** data
5. **Analyze** data

---

---

- **207. NumPy Interview Questions**

---

### **1. How will you reverse the NumPy array using one line of code?**

This can be done using slicing as shown below:

```python
python
CopyEdit
reversed_array = arr[::-1]

```

Where `arr` is the original array, and `reversed_array` is the result after reversing all elements in `arr`.

---

---

- **208. How will you find the nearest value in a given NumPy array?**

We can use the `argmin()` method of NumPy:

```python
python
CopyEdit
import numpy as np

def find_nearest_value(arr, value):
    arr = np.asarray(arr)
    idx = (np.abs(arr - value)).argmin()
    return arr[idx]

# Example usage
arr = np.array([0.21169, 0.61391, 0.6341, 0.0131, 0.16541, 0.5645, 0.5742])
value = 0.52
print(find_nearest_value(arr, value))  # Output: 0.5645

```

---

---

- **209. How will you sort an array based on the Nth column?**

Example: Sorting an array `arr` by the second column.

```python
python
CopyEdit
import numpy as np

arr = np.array([[8, 3, 2],
                [3, 6, 5],
                [6, 1, 4]])

# Sorting by the second column
arr = arr[arr[:, 1].argsort()]
print(arr)

```

**Output:**

```
lua
CopyEdit
[[6 1 4]
 [8 3 2]
 [3 6 5]]

```

---

---

- **210. How will you read CSV data into a NumPy array?**

We can use `genfromtxt()` with a comma as a delimiter:

```python
python
CopyEdit
from numpy import genfromtxt
csv_data = genfromtxt('sample_file.csv', delimiter=',')

```

---

---

- **211. How will you efficiently load data from a text file?**

Use the `numpy.loadtxt()` function:

```python
python
CopyEdit
import numpy as np
data = np.loadtxt('file.txt', delimiter=',')

```

Other efficient file formats:

- **Text files**: Slow but human-readable.
- **Raw binary files**: Fast but not portable.
- **Pickle**: Portable but version-dependent.

---

- **HDF5**: Supports large datasets.
- **`.npy` format**: Simple, efficient, and portable.

---

---

- **212. How will you replace the second column in a NumPy array with new values?**

Example:

```python
python
CopyEdit
import numpy as np

# Original array
inputArray = np.array([[35, 53, 63], [72, 12, 22], [43, 84, 56]])
new_col = np.array([[20, 30, 40]]).T  # Transpose to make it a column vector

# Delete 2nd column
arr = np.delete(inputArray, 1, axis=1)

# Insert new column
arr = np.insert(arr, 1, new_col, axis=1)

print(arr)

```

---

---

- **213. What are the steps to create 1D, 2D, and 3D arrays?**

---

- **1D Array**

```python
python
CopyEdit
import numpy as np
one_dimensional_arr = np.array([1, 2, 4])
print("1D array:", one_dimensional_arr)

```

---

- **2D Array**

```python
python
CopyEdit
two_dimensional_arr = np.array([[1, 2, 3], [4, 5, 6]])
print("2D array:", two_dimensional_arr)

```

---

- **3D Array**

```python
python
CopyEdit
three_dimensional_arr = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]]])
print("3D array:", three_dimensional_arr)

```

---

- **ND Array (6D Example)**

```python
python
CopyEdit
ndArray = np.array([1, 2, 3, 4], ndmin=6)
print("ND array:", ndArray)
print('Dimensions of array:', ndArray.ndim)

```

---

---

- **214. How are NumPy arrays advantageous over Python lists?**

Python lists are versatile but have limitations when performing mathematical operations like element-wise addition or multiplication. The key advantages of **NumPy arrays** over Python lists are:

- **Performance**: NumPy is around **30x faster** than Python lists for large data due to optimized memory usage and vectorized operations.
- **Memory Efficiency**: NumPy arrays store elements of the **same type** in contiguous memory locations, reducing overhead.
- **Vectorized Operations**: Unlike Python lists, NumPy allows **element-wise computations** without explicit loops, making it more efficient for numerical tasks.
- **Built-in Functions**: NumPy offers a variety of mathematical functions for **linear algebra, statistics, and trigonometry**, making it ideal for scientific computing.

---

---

- **215. What do you understand by NumPy?**

NumPy (**NUMerical PYthon**) is a **powerful, open-source** Python library for numerical computing. It provides:

- **Efficient N-Dimensional Array Handling**: Supports **1D, 2D, and multi-dimensional arrays** for complex computations.
- **Mathematical Functions**: Offers tools for **trigonometry, linear algebra, and statistical analysis**.
- **High Performance**: Optimized for fast execution with **vectorized operations**.
- **Broadcasting**: Enables efficient operations between arrays of different shapes.
- **Integration with Other Libraries**: Commonly used in **data science, machine learning, and AI** with libraries like Pandas, TensorFlow, and SciPy.

NumPy is widely used in scientific computations, machine learning, and data analysis due to its flexibility and efficiency.

---

---

- **216. How will you find the shape of any given NumPy array?**

The **shape** of a NumPy array can be found using the `.shape` attribute, which returns a tuple representing the dimensions of the array.

```python
python
CopyEdit
import numpy as np

arr_two_dim = np.array([["x1", "x2", "x3", "x4"],
                        ["x5", "x6", "x7", "x8"]])

arr_one_dim = np.array([3, 2, 4, 5, 6])

# Find and print shape
print("2-D Array Shape: ", arr_two_dim.shape)
print("1-D Array Shape: ", arr_one_dim.shape)

```

**Output:**

```
mathematica
CopyEdit
2-D Array Shape:  (2, 4)
1-D Array Shape:  (5,)

```

- The **first value** in `.shape` represents the **number of rows**.
- The **second value** represents the **number of columns** (if applicable).
- For **1D arrays**, the `.shape` attribute returns a single-element tuple.

---

---

- **217. Differentiate between deep and shallow copies.**

- **Shallow Copy**:
  - Creates a **new object** but stores **references** of original elements.
  - Does **not** recursively copy nested objects.
  - Uses `copy.copy()` in Python.
- **Deep Copy**:
  - Creates a **completely independent** copy of an object.
  - Recursively copies **all nested objects**.
  - Uses `copy.deepcopy()` in Python.

---

---

- **218. What is the main function in Python? How do you invoke it?**

Python does not have an explicit `main()` function like other languages, but we can simulate it using the `__name__` variable.

```python
python
CopyEdit
def main():
   print("Hi Interviewbit!")

if __name__ == "__main__":
   main()

```

- `__name__ == "__main__"` ensures that `main()` runs only when the script is executed directly, not when imported.

---

---

- **219. Are there any tools for identifying bugs and performing static analysis in Python?**

Yes, the following tools help in **bug detection** and **static analysis**:

- **PyChecker**: Identifies **bugs and errors** in Python source code.
- **Pylint**: Checks for **coding standards**, linting, and potential issues.

---

---

- **220. Define PIP.**

- **PIP (Python Installer Package)** is a **package manager** for installing Python modules.
- It searches for packages online and installs them into the working environment.
- Syntax for installing a package:
  ```
  sh
  CopyEdit
  pip install <package_name>

  ```

---

---

- **221. Define PYTHONPATH.**

- **PYTHONPATH** is an **environment variable** that tells Python where to look for modules.
- Used to include additional directories when importing a module.

---

---

- **222. Define GIL.**

- **GIL (Global Interpreter Lock)** is a **mutex** that prevents multiple threads from executing Python bytecode **simultaneously**.
- It ensures thread **synchronization** but prevents true **parallel execution** in multi-threaded programs.

---

---

- **223. What are the differences between pickling and unpickling?**

- **Pickling**: Converts Python objects into a **binary format** using `pickle.dump()`.
- **Unpickling**: Converts binary data back into **Python objects** using `pickle.load()`.

Example:

```python
python
CopyEdit
import pickle

data = {'name': 'Alice', 'age': 25}

# Pickling
with open('data.pkl', 'wb') as file:
    pickle.dump(data, file)

# Unpickling
with open('data.pkl', 'rb') as file:
    loaded_data = pickle.load(file)

print(loaded_data)  # Output: {'name': 'Alice', 'age': 25}

```

---

---

- **224. Can you easily check if all characters in a given string are alphanumeric?**

Yes, using `isalnum()`:

```python
python
CopyEdit
print("abdc1321".isalnum())  # Output: True
print("xyz@123$".isalnum())  # Output: False

```

Or using **regex**:

```python
python
CopyEdit
import re

print(bool(re.match('[A-Za-z0-9]+$', 'abdc1321')))  # Output: True
print(bool(re.match('[A-Za-z0-9]+$', 'xyz@123$')))  # Output: False

```

---

---

- **225. How can you generate random numbers in Python?**

Using the `random` module:

- **Generate a random float (0 to 1):**
  ```python
  python
  CopyEdit
  import random
  print(random.random())

  ```
- **Generate a random integer in a range:**
  ```python
  python
  CopyEdit
  print(random.randint(1, 100))  # Random number between 1 and 100

  ```
- **Generate a random number with a step:**
  ```python
  python
  CopyEdit
  print(random.randrange(5, 100, 2))  # Random even number between 5 and 100

  ```

---

---

- **226. What are lambda functions?**

- **Lambda functions** are **anonymous, single-expression functions**.
- Used for **short, simple** operations.

Example:

```python
python
CopyEdit
mul_func = lambda x, y: x * y
print(mul_func(6, 4))  # Output: 24

```

---

---

- **227. What are some of the most commonly used built-in modules in Python?**

- **`os`**: Interacts with the operating system.
- **`math`**: Provides mathematical functions.
- **`sys`**: Provides system-specific functions.
- **`random`**: Generates random numbers.
- **`re`**: Supports **regular expressions**.
- **`datetime`**: Works with dates and times.
- **`json`**: Handles JSON data.

---

---

- **228. Differentiate between a package and a module in Python.**

| Feature    | Module                                     | Package                                      |
| ---------- | ------------------------------------------ | -------------------------------------------- |
| Definition | A **single** Python file (`.py`)           | A **collection** of modules in a directory   |
| Structure  | Contains **functions, classes, variables** | Contains **multiple modules & sub-packages** |
| Example    | `math.py`                                  | `numpy` package (contains multiple modules)  |
| Creation   | Create a file: `my_module.py`              | Create a folder with an `__init__.py` file   |

**Creating a package**:

1. Create a **directory** with a meaningful name.
2. Place **modules** inside the directory.
3. Add an **`__init__.py`** file (can be empty or contain initialization code).

---

---

- **229. How will you access the dataset of a publicly shared spreadsheet in CSV format stored in Google Drive?**

We can use the `requests` module to fetch the data and `pandas` to read the CSV file. The `StringIO` module from `io` is used to handle the content as a file-like object.

### **Corrected Code:**

```python
python
CopyEdit
import pandas as pd
import requests
from io import StringIO

# Public Google Sheets CSV link
csv_link = "https://docs.google.com/spreadsheets/d/.../export?format=csv"

# Fetch content from Google Drive link
response = requests.get(csv_link)
data_source = StringIO(response.text)

# Read CSV into DataFrame
dataframe = pd.read_csv(data_source)

# Print first few rows
print(dataframe.head())

```

### **Explanation:**

1. **`requests.get(csv_link).text`** fetches the raw CSV content.
2. **`StringIO(response.text)`** converts the text data into a file-like object.
3. **`pd.read_csv(data_source)`** reads the CSV content into a Pandas DataFrame.
4. **`.head()`** displays the first few rows of the dataset.

---

---

- **230. Write a Program to combine two different dictionaries. If keys are the same, add their values.**

We can use the `Counter` method from the `collections` module.

```python
python
CopyEdit
from collections import Counter

d1 = {'key1': 50, 'key2': 100, 'key3': 200}
d2 = {'key1': 200, 'key2': 100, 'key4': 300}

# Combine dictionaries, adding values for duplicate keys
new_dict = Counter(d1) + Counter(d2)

print(new_dict)

```

---

---

- **231. Convert date from yyyy-mm-dd format to dd-mm-yyyy format.**

### **Using the `re` module:**

```python
python
CopyEdit
import re

def transform_date_format(date):
    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', r'\3-\2-\1', date)

date_input = "2021-08-01"
print(transform_date_format(date_input))  # Output: 01-08-2021

```

### **Using the `datetime` module:**

```python
python
CopyEdit
from datetime import datetime

new_date = datetime.strptime("2021-08-01", "%Y-%m-%d").strftime("%d-%m-%Y")
print(new_date)  # Output: 01-08-2021

```

---

---

- **232. Match a string that has the letter ‘a’ followed by 4 to 8 'b’s.**

```python
python
CopyEdit
import re

def match_text(txt_data):
    pattern = r'ab{4,8}'  # Matches 'a' followed by 4 to 8 'b's
    return 'Match found' if re.search(pattern, txt_data) else 'Match not found'

print(match_text("abc"))        # Output: Match not found
print(match_text("aabbbbbc"))   # Output: Match found

```

---

---

- **233. Solve the system of equations:**

ax+by=cax + by = c

ax+by=c

mx+ny=omx + ny = o

mx+ny=o

```python
python
CopyEdit
a, b, c, m, n, o = 5, 9, 4, 7, 9, 4

temp = a * n - b * m
if temp != 0:
    x = (c * n - b * o) / temp
    y = (a * o - m * c) / temp
    print(x, y)

```

---

---

- **234. Add two integers greater than 0 without using the plus (+) operator.**

We use bitwise operations.

```python
python
CopyEdit
def add_nums(num1, num2):
    while num2 != 0:
        carry = num1 & num2
        num1 = num1 ^ num2
        num2 = carry << 1
    return num1

print(add_nums(2, 10))  # Output: 12

```

---

---

- **235. Find pairs in an array whose sum equals a target value.**

Using a hash set for efficient lookup.

```python
python
CopyEdit
def print_pairs(arr, N):
    hash_set = set()

    for num in arr:
        val = N - num
        if val in hash_set:
            print(f"Pair: ({num}, {val})")
        hash_set.add(num)

# Driver code
arr = [1, 2, 40, 3, 9, 4]
N = 3
print_pairs(arr, N)

```

---

---

- **236. Count the occurrences of every character in a given text file.**

Using `collections.Counter`.

```python
python
CopyEdit
import collections
import pprint

with open("sample_file.txt", 'r') as data:
    count_data = collections.Counter(data.read().upper())

count_value = pprint.pformat(count_data)
print(count_value)

```

---

---

- **237. Check if all numbers in a sequence are unique.**

Using `set()` to check for uniqueness.

```python
python
CopyEdit
def check_distinct(data_list):
    return len(data_list) == len(set(data_list))

print(check_distinct([1,6,5,8]))     # Output: True
print(check_distinct([2,2,5,5,7,8])) # Output: False

```

---

---

- **238. Write a Python function that takes a variable number of arguments.**

Using `*args` to accept variable-length arguments.

```python
python
CopyEdit
def func(*var):
    for i in var:
        print(i)

func(1)
func(20, 1, 6)

```

---

---

- **239. What is Python, and what are its key features?**

Python is a versatile, high-level programming language known for its easy-to-read syntax and broad applications.

### **Key Features of Python:**

- **Simple and Readable Syntax:** Python’s syntax is clean and easy to understand.
- **Interpreted Language:** Executes code line by line, making debugging easier.
- **Dynamic Typing:** No need to declare variable types explicitly.
- **Extensive Libraries and Frameworks:** Libraries like `NumPy`, `Pandas`, and `Django` make Python powerful.
- **Cross-Platform Compatibility:** Runs on Windows, macOS, and Linux.

---

---

- **240. What are Python lists and tuples?**

### **Lists:**

- **Mutable:** Elements can be changed.
- **Memory Usage:** Uses more memory.
- **Performance:** Slower than tuples but supports insertion and deletion.
- **Methods:** Offers various built-in methods.

```python
python
CopyEdit
a_list = ["Data", "Camp", "Tutorial"]
a_list.append("Session")
print(a_list)  # Output: ['Data', 'Camp', 'Tutorial', 'Session']

```

### **Tuples:**

- **Immutable:** Elements cannot be changed.
- **Memory Usage:** Uses less memory.
- **Performance:** Faster than lists.
- **Methods:** Limited built-in methods.

```python
python
CopyEdit
a_tuple = ("Data", "Camp", "Tutorial")
print(a_tuple)  # Output: ('Data', 'Camp', 'Tutorial')

```

---

---

- **241. What is init() in Python?**

The `__init__()` method is a **constructor** in Object-Oriented Programming (OOP). It initializes an object's state when it is created.

### **Example:**

```python
python
CopyEdit
class BookShop:
    def __init__(self, title):
        self.title = title  # Initialize object attribute

    def book(self):
        print('The title of the book is', self.title)

b = BookShop('Sandman')
b.book()  # Output: The title of the book is Sandman

```

---

---

- **242. Explain List, Dictionary, and Tuple Comprehensions with Examples?**

### **List Comprehension:**

```python
python
CopyEdit
my_list = [i for i in range(1, 10)]
print(my_list)  # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]

```

### **Dictionary Comprehension:**

```python
python
CopyEdit
my_dict = {i: i**2 for i in range(1, 10)}
print(my_dict)
# Output: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81}

```

### **Tuple Comprehension (Generator Expression):**

```python
python
CopyEdit
my_tuple = (i for i in range(1, 10))
print(my_tuple)  # Output: <generator object <genexpr> at 0x7fb91b151430>
print(tuple(my_tuple))  # Converts generator to tuple

```

---

---

- **243. Basic Python Interview Questions**

---

### **1. What is Python, and what are its key features?**

Python is a versatile, high-level programming language known for its easy-to-read syntax and broad applications.

### **Key Features of Python:**

- **Simple and Readable Syntax:** Python’s syntax is clean and easy to understand.
- **Interpreted Language:** Executes code line by line, making debugging easier.
- **Dynamic Typing:** No need to declare variable types explicitly.
- **Extensive Libraries and Frameworks:** Libraries like `NumPy`, `Pandas`, and `Django` make Python powerful.
- **Cross-Platform Compatibility:** Runs on Windows, macOS, and Linux.

---

---

- **244. Intermediate Python Interview Questions**

---

### **6. What is the Global Interpreter Lock (GIL) in Python, and why is it important?**

The Global Interpreter Lock (GIL) is a mutex used in CPython (the standard Python interpreter) to prevent multiple native threads from executing Python bytecode simultaneously. It simplifies memory management but limits multi-threading performance for CPU-bound tasks. This makes threading in Python less effective for certain tasks, though it works well for I/O-bound operations.

---

---

- **245. Can you explain common searching and graph traversal algorithms in Python?**

Python has a number of powerful algorithms for searching and graph traversal:

- **Binary Search:** Efficient for finding an item in a sorted list by repeatedly dividing the search range in half.
- **AVL Tree:** A self-balancing binary search tree that maintains balance to ensure efficient searches, insertions, and deletions.
- **Breadth-First Search (BFS):** Explores a graph level by level, making it ideal for finding the shortest path in an unweighted graph.
- **Depth-First Search (DFS):** Explores as far as possible down each branch before backtracking; useful for tasks like maze-solving.
- *A Algorithm:*A heuristic-based algorithm used in pathfinding for maps and games, combining the benefits of BFS and DFS.

---

---

- **246. What is a KeyError in Python, and how can you handle it?**

A `KeyError` occurs when you try to access a key that doesn’t exist in a dictionary.

### **Ways to handle a KeyError:**

1. **Use the `.get()` method:**

```
data = {'name': 'Alice'}
print(data.get('age', 'Key not found'))  # Output: Key not found
```

1. **Use a try-except block:**

```
try:
    print(data['age'])
except KeyError:
    print("Key does not exist!")
```

1. **Check for the key using `in`:**

```
if 'age' in data:
    print(data['age'])
```

---

---

- **247. Advanced Python Interview Questions**

---

### **12. What is monkey patching in Python?**

Monkey patching is a dynamic technique that modifies classes or modules at runtime.

### **Example:**

```
class Monkey:
    def patch(self):
        print("patch() is being called")

def monk_p(self):
    print("monk_p() is being called")

# Replacing address of "patch" with "monk_p"
Monkey.patch = monk_p

obj = Monkey()
obj.patch()  # Output: monk_p() is being called
```

Monkey patching allows runtime modification of a module, class, or method, but should be used cautiously as it can lead to unpredictable behavior.

---

---

- **248. What is the Python with statement designed for?**

The `with` statement is used for exception handling to make code cleaner and simpler. It is generally used for the management of common resources like creating, editing, and saving a file.

**Example:**

```
# Using with statement
with open('myfile.txt', 'w') as file:
    file.write('DataCamp Black Friday Sale!!!')
```

---

---

- **249. Why use else in try/except construct in Python?**

`try:` and `except:` are commonly used for exception handling in Python, but `else:` is triggered when no exception is raised.

**Example:**

```
try:
    num1 = int(input('Enter Numerator: '))
    num2 = int(input('Enter Denominator: '))
    division = num1 / num2
    print(f'Result is: {division}')
except:
    print('Invalid input!')
else:
    print('Division is successful.')
```

**Try 1:**

```
Enter Numerator: 2
Enter Denominator: d
Invalid input!
```

**Try 2:**

```
Enter Numerator: 2
Enter Denominator: 1
Result is: 2.0
Division is successful.
```

---

---

- **250. What are context managers in Python, and how are they implemented?**

Context managers in Python manage resources, ensuring they are properly acquired and released. The most common use of context managers is the `with` statement.

**Example:**

```
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

with FileManager('test.txt', 'w') as f:
    f.write('Hello, world!')
```

---

---

- **251. What are metaclasses in Python, and how do they differ from regular classes?**

Metaclasses are classes of classes. They define how classes behave and are created. While regular classes create objects, metaclasses create classes.

**Example:**

```
class Meta(type):
    def __new__(cls, name, bases, dct):
        print(f"Creating class {name}")
        return super().__new__(cls, name, bases, dct)

class MyClass(metaclass=Meta):
    pass
```

**Output:**

```
Creating class MyClass
```

---

---

- **252. Python Data Science Interview Questions**

---

### 18. What are the advantages of NumPy over regular Python lists?

1. **Memory Efficiency**: NumPy arrays consume less memory.
2. **Speed**: NumPy arrays perform operations faster than lists.
3. **Versatility**: NumPy arrays support vectorized operations, making them more convenient than lists.

**Example:**

```
import numpy as np
import sys

# List memory usage
list_data = range(1000)
print("List Memory Usage:", sys.getsizeof(5) * len(list_data))

# NumPy array memory usage
numpy_data = np.arange(1000)
print("NumPy Array Memory Usage:", numpy_data.size * numpy_data.itemsize)
```

---

---

- **253. What is the difference between merge, join, and concatenate?**

### **Merge**

Merges two DataFrames using a common column.

```
import pandas as pd

# Sample DataFrames
df1 = pd.DataFrame({'Id': [1, 2, 3], 'Name': ['A', 'B', 'C']})
df2 = pd.DataFrame({'Id': [1, 2, 3], 'Score': [90, 85, 88]})

# Merge DataFrames
merged_df = pd.merge(df1, df2, how='outer', on='Id')
print(merged_df)
```

### **Join**

Joins two DataFrames using the index.

```
df1 = df1.set_index('Id')
df2 = df2.set_index('Id')
joined_df = df1.join(df2)
print(joined_df)
```

### **Concatenate**

Concatenates two or more DataFrames along a specific axis.

```
df_concat = pd.concat([df1, df2], axis=1)
print(df_concat)
```

---

### **Key Differences:**

- `join()`: Combines DataFrames by index.
- `merge()`: Combines DataFrames using a specified column.
- `concat()`: Stacks DataFrames either vertically or horizontally.

---

---

- **254. How do you identify and deal with missing values?**

### Identifying Missing Values

We can identify missing values in a DataFrame using the `isnull()` function along with `sum()`. The `isnull()` function returns boolean values, and `sum()` provides the number of missing values in each column.

### Example:

```python
python
CopyEdit
import pandas as pd
import numpy as np

# Dictionary of lists
data = {'id': [1, 4, np.nan, 9],
        'Age': [30, 45, np.nan, np.nan],
        'Score': [np.nan, 140, 180, 198]}

# Creating a DataFrame
df = pd.DataFrame(data)

# Identifying missing values
df.isnull().sum()

```

**Output:**

```
bash
CopyEdit
id       1
Age      2
Score    1

```

### Dealing with Missing Values

There are multiple ways to handle missing values:

1. **Drop missing values** (not recommended for small datasets):

```python
python
CopyEdit
df.dropna(axis=0, how='any')

```

1. **Fill missing values using `fillna()`** (e.g., forward or backward fill):

```python
python
CopyEdit
df.fillna(method='bfill')

```

1. **Replace missing values with a constant value:**

```python
python
CopyEdit
df.replace(to_replace=np.nan, value=-999)

```

1. **Use interpolation to estimate missing values:**

```python
python
CopyEdit
df.interpolate(method='linear', limit_direction='forward')

```

**Note:** Avoid `dropna()` in small datasets, as it may lead to data loss.

---

---

- **255. Which Python libraries have you used for visualization?**

Data visualization is crucial for data analysis. Some commonly used Python visualization libraries include:

- **Matplotlib** – Basic 2D plots (scatter, line, bar, etc.).
- **Seaborn** – Statistical visualization built on Matplotlib.
- **Plotly** – Interactive visualizations with zoom and animation.
- **Bokeh** – High-level interactive charts for web applications.

### Example using Matplotlib and Seaborn:

```python
python
CopyEdit
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data
x = [1, 2, 3, 4, 5]
y = [10, 15, 7, 12, 8]

# Line plot with Matplotlib
plt.plot(x, y, marker='o', linestyle='--')
plt.title('Matplotlib Line Plot')
plt.show()

# Seaborn Box Plot
sns.boxplot(y=[10, 15, 7, 12, 8])
plt.title('Seaborn Box Plot')
plt.show()

```

For interactive dashboards, **Plotly** and **Bokeh** are preferred.

---

---

- **256. How would you normalize or standardize a dataset in Python?**

- **Normalization** scales data to a fixed range, usually **[0, 1]**.
- **Standardization** transforms data to have a **mean of 0** and a **standard deviation of 1**.

### Example using `sklearn`:

```python
python
CopyEdit
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np

# Sample data
data = np.array([[1, 2], [3, 4], [5, 6]])

# Normalize (scale between 0 and 1)
normalizer = MinMaxScaler()
normalized = normalizer.fit_transform(data)
print(normalized)

# Standardize (mean=0, std=1)
scaler = StandardScaler()
standardized = scaler.fit_transform(data)
print(standardized)

```

---

---

- **257. How can you replace spaces with a given character in Python?**

We can replace spaces in a string using iteration or the `replace()` method.

---

### Example 1: Using a loop

```python
python
CopyEdit
def str_replace(text, ch):
    result = ''
    for i in text:
        if i == ' ':
            i = ch
        result += i
    return result

text = "D t C mpBl ckFrid yS le"
ch = "a"

print(str_replace(text, ch))  # Output: "DataCampBlackFridaySale"
```

---

### Example 2: Using `replace()`

```python
python
CopyEdit
text = "l vey u"
ch = "o"
text.replace(" ", ch)  # Output: "loveyou"
```

---

---

- **258. What is an abstract method in Python?**

An **abstract method** is a method that is declared in a base (parent) class but contains no implementation (no code body). It acts as a contract, forcing any concrete (non-abstract) subclass that inherits from the base class to provide its own specific implementation for that method.

If a subclass does not implement the abstract method, Python raises a `TypeError` at instantiation time.

In Python, abstract methods are defined using the `@abstractmethod` decorator from the built-in `abc` (Abstract Base Classes) module:

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self) -> str:
        pass

class Dog(Animal):
    def make_sound(self) -> str:
        return "Woof!"

# Instantiating Animal directly or a subclass that hasn't implemented make_sound
# will raise a TypeError.
dog = Dog()
print(dog.make_sound())  # Output: Woof!
```

---

---

- **259. What are the four core concepts of Object-Oriented Programming (OOP), and how are they implemented in Python?**

Object-Oriented Programming (OOP) is a programming paradigm that organizes software design around **objects** (data/state) rather than functions and logic. The four pillar concepts are:

---

### 1. Encapsulation (Data Hiding & Protection)
Encapsulation is the practice of bundling data (attributes) and the methods that operate on that data inside a single unit (a class), while restricting direct access to some of the object's components.
* **Why it matters:** It prevents external code from accidentally modifying internal object states, enforcing data validation through getters and setters.
* **In Python:** Python does not have strict `private` keywords. Instead, it uses naming conventions:
  * `_variable`: Protected (a warning to other developers not to access it directly).
  * `__variable`: Private (triggers name mangling under the hood to prevent direct access).

```python
class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.__balance = balance  # Private attribute

    # Getter
    def get_balance(self) -> float:
        return self.__balance

    # Setter with validation
    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount
        else:
            raise ValueError("Deposit amount must be positive")

account = BankAccount("Alice", 1000.0)
# account.__balance  # Throws AttributeError
account.deposit(500)
print(account.get_balance())  # Output: 1500.0
```

---

### 2. Inheritance (Code Reuse)
Inheritance allows a new class (subclass/child) to adopt the attributes and methods of an existing class (superclass/parent).
* **Why it matters:** It promotes code reuse and creates hierarchical relationships.
* **In Python:** You pass the parent class name in parentheses when defining the child class. Python also supports multiple inheritance.

```python
class Vehicle:
    def __init__(self, brand: str):
        self.brand = brand

    def start_engine(self):
        return f"{self.brand} engine started."

class Car(Vehicle):  # Car inherits from Vehicle
    def drive(self):
        return f"{self.brand} is driving."

my_car = Car("Tesla")
print(my_car.start_engine())  # Output: Tesla engine started. (Inherited method)
print(my_car.drive())         # Output: Tesla is driving.
```

---

### 3. Polymorphism (Many Forms)
Polymorphism allows different classes to define methods with the same name but different implementations. It enables you to treat objects of different types uniformly.
* **Why it matters:** It allows you to write flexible, generic code that works with any object that follows a specific interface.
* **In Python:** Python achieves polymorphism through method overriding and its dynamic "Duck Typing" nature.

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

def make_animal_speak(animal):
    # This function doesn't care if it's a Dog or a Cat, as long as it has a speak() method.
    print(animal.speak())

make_animal_speak(Dog())  # Output: Woof!
make_animal_speak(Cat())  # Output: Meow!
```

---

### 4. Abstraction (Hiding Complexity)
Abstraction hides complex implementation details and only exposes the essential interface or features to the user.
* **Why it matters:** It reduces complexity by hiding the "how" and only showing the "what."
* **In Python:** Handled using the `abc` module to define Abstract Base Classes (ABCs) and `@abstractmethod` decorators.

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float):
        pass

class StripeProcessor(PaymentProcessor):
    def process_payment(self, amount: float):
        # Specific, complex Stripe API integration goes here
        return f"Processing ${amount} via Stripe API"

# payment = PaymentProcessor()  # Raises TypeError (cannot instantiate abstract class)
processor = StripeProcessor()
print(processor.process_payment(250.0))  # Output: Processing $250.0 via Stripe API
```

---
