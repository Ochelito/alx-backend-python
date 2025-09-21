# ALX Backend Python - Unit and Integration Testing

## Overview
This repository contains Python unit and integration tests for the `utils.py` and `client.py` modules, focusing on GithubOrgClient operations. All tests are written following `pycodestyle` standards, using `unittest` and `parameterized` for parameterization and mocking.

---

## Requirements
- Python 3.7 (Ubuntu 18.04 LTS)
- All Python files are executable and start with:
  ```bash
  #!/usr/bin/env python3
  ```
- Code style follows `pycodestyle` v2.5.
- All modules, classes, and functions include documentation with clear purpose descriptions.
- Type annotations are used throughout.

---

## Project Structure
```
0x03-Unittests_and_integration_tests/
├── fixtures.py
├── utils.py
├── client.py
├── test_utils.py
├── test_client.py
└── README.md
```

### Fixtures
`fixtures.py` contains sample payloads for integration tests, including:
- `org_payload`
- `repos_payload`
- `expected_repos`
- `apache2_repos`

---

## Tasks Overview

### Task 0: Parameterize a Unit Test
- Tested `utils.access_nested_map` for several nested maps.
- Used `@parameterized.expand` for different paths.

### Task 1: Unit Test Exception Handling
- Tested `access_nested_map` raises `KeyError` when path is invalid.
- Verified exception messages.

### Task 2: Mock HTTP Calls
- Tested `utils.get_json` without real HTTP requests.
- Used `unittest.mock.patch` to mock `requests.get`.
- Verified the JSON output and call count.

### Task 3: Test Memoization
- Tested `utils.memoize` decorator.
- Ensured the decorated method is called only once even when accessed multiple times.

### Task 4: Parameterize and Patch as Decorators
- Tested `GithubOrgClient.org` method.
- Used `@patch` to mock `get_json` and `@parameterized.expand` for multiple orgs.
- Verified correct payload and URL usage.

### Task 5: Mocking a Property
- Tested `_public_repos_url` property.
- Used `patch` with `PropertyMock` to mock `org` payload.

### Task 6: More Patching
- Tested `public_repos()` method.
- Mocked `_public_repos_url` property and `get_json` to ensure correct repo list.
- Verified both were called exactly once.

### Task 7: Parameterize License Checks
- Tested `has_license` static method.
- Used `@parameterized.expand` to check different license keys.

### Task 8: Integration Test Setup with Fixtures
- Created `TestIntegrationGithubOrgClient`.
- Used `@parameterized_class` with fixtures.
- Mocked `requests.get` using a `side_effect` function to return appropriate payloads for URLs.
- Implemented `setUpClass` and `tearDownClass` to start and stop the patcher.

### Task 9: Integration Tests for Public Repos
- Implemented `test_public_repos` to verify full repo list.
- Implemented `test_public_repos_with_license` to verify filtering by `apache-2.0` license.
- Tests use the fixture data to ensure consistency.

---

## Running Tests
1. Make sure you are in the `0x03-Unittests_and_integration_tests` directory.
2. Run all unit and integration tests:
```bash
python3 -m unittest discover
```
3. Run only `utils` tests:
```bash
python3 -m unittest test_utils.py
```
4. Run only `client` integration tests:
```bash
python3 -m unittest test_client.py
```

---

## Notes
- All external HTTP calls are mocked; tests can run offline.
- Ensure `fixtures.py` contains accurate payloads matching expected test results.
- All files are executable and conform to style and documentation requirements.

---

## Authors
- Idoko Augustine (ALX Backend Python)

---

## License
MIT License

