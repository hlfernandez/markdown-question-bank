Which of the following options best describes the purpose of the `range(3)` function in Python?

- Creates a list with the numbers 1, 2, and 3.
- [X] Creates an iterator that produces the numbers 0, 1, and 2.
- Creates a string with the characters '0', '1', '2'.

---

Given the Python code from [this appendix](#code-1), indicate what its behavior and console output would be:

- [X] The function reverses the string.
  The output would be: `cba`.
- The function removes the first letter and prints the remaining string.
  The output would be: `bc`.
- The function transforms the string to uppercase.
  The output would be: `ABC`.

---

What type of structure does the `enumerate()` function return when applied to a list?

- [X] An iterator of tuples with the index and the corresponding element.
- A dictionary where each key is an index and the value is an element.
- A list with the index followed by the element.

---

What is the result of `len("Python")`?

- 5
- [X] 6
- 7

---

What does `print(2 ** 3)` produce in Python?

- 5
- 6
- [X] 8

---

What does `list.append(x)` do?

- Adds the element `x` to the beginning of the list.
- [X] Adds the element `x` to the end of the list.
- Adds the element `x` in order in the list.

---

What does it mean for a function to be **recursive**?

- That it automatically calls other functions.
- That it runs in parallel with others.
- [X] That it calls itself.

---

What does `True and False` produce?

- True
- [X] False
- Error

---

What is the purpose of `def` in Python?

- To declare a class.
- [X] To define a function.
- To create a global variable.

---

When does an `IndexError` exception occur?

- [X] When trying to access an index outside the range of a list.
- When dividing by zero.
- When accessing a key in a dictionary.

---

What type of data does `{"a": 1, "b": 2}` represent?

- List
- [X] Dictionary
- Tuple

| Difficulty  | TeachScore |
|-------------|------------|
| Low         | 1          |

---

Considering the initial assignment of variable A in the first line, indicate the case in which the value displayed for variable A is modified after executing the other two instructions:

- 
    ```python
    A = 'Programming II'
    B = A
    B = '2025'
    ```
- [X]
    ```python
    A= ['Programming II']
    B = A
    B[0] = '2025'
    ```
- 
    ```python
    A= ['Programming II']
    B = A[:]
    B[0] = '2025'
    ```

| Difficulty  | TeachScore |
|-------------|------------|
| High        | 10         |

---

What does `"  texto  ".strip()` do?

- [X] Removes spaces at the beginning and the end.
- Removes all spaces.
- Converts to uppercase.

# Appendices

## Code 1

```python
def misterio(x):
    return x[::-1]

print(misterio("abc"))
```
