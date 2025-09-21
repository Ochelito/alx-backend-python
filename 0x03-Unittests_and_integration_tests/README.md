# 0x03. Unittests and Integration Tests

This project is part of the **ALX Backend Python** curriculum.  
It introduces **unit testing** and **integration testing** in Python using the `unittest` framework, the `parameterized` library, and mocking techniques.

---

## 📌 Project Requirements
- Files interpreted/compiled on **Ubuntu 18.04 LTS** using **Python 3.7**  
- All files must:
  - End with a new line  
  - Start with `#!/usr/bin/env python3`  
  - Be executable  
- Code must follow **pycodestyle** (PEP8) version **2.5**  
- All modules, classes, and functions must contain **docstrings**  
- All functions and coroutines must have **type annotations**  

---

## 📚 Learning Objectives
- Understand the difference between **unit tests** and **integration tests**  
- Write **parameterized tests** to reduce repetition  
- Use **mocks** to test functions that depend on external resources (e.g., API calls)  
- Apply the **memoization** pattern in testing  

---

## 📂 Project Structure
0x03-Unittests_and_integration_tests/
│── utils.py # Utility functions (access_nested_map, get_json, memoize)
│── test_utils.py # Unit tests for utils.py
│── client.py # Client class
│── fixtures.py # Test fixtures
│── README.md # Project documentation