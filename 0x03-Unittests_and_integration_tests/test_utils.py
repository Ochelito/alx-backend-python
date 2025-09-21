#!/usr/bin/env python3
"""Unit tests for utils module."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected) -> None:
        """Test that access_nested_map returns expected results."""
        self.assertEqual(
            access_nested_map(nested_map, path),
            expected
        )

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map,
        path,
        expected_message
    ) -> None:
        """Test that access_nested_map raises KeyError with the correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(
            str(cm.exception),
            f"'{expected_message}'"
        )


class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get) -> None:
        """Test that get_json returns expected result with mocked HTTP call."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test cases for the memoize decorator."""

    def test_memoize(self) -> None:
        """Test that memoize caches the result of a method."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass,
            "a_method",
            return_value=42
        ) as mock_method:
            obj = TestClass()

            # Call the memoized property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Both results should be the same
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # a_method should only be called once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
