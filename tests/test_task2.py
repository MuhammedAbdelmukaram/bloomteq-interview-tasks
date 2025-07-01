import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from task2.logic import lookup  # Import lookup from logic module


class TestLookupFunction(unittest.TestCase):

    # === Basic Valid Lookups ===

    def test_valid_single_level_lookup(self):
        self.assertEqual(lookup({"key": "value"}, "key"), "value")

    def test_valid_nested_lookup(self):
        self.assertEqual(lookup({"a": {"b": {"c": "value"}}}, "a.b.c"), "value")

    def test_integer_keys_as_strings(self):
        self.assertEqual(lookup({"a": {"1": {"2": "x"}}}, "a.1.2"), "x")

    def test_integer_keys(self):
        self.assertEqual(lookup({"a": {1: {2: "value"}}}, "a.1.2"), "value")

    def test_list_in_value(self):
        self.assertEqual(lookup({"a": {"b": [1, 2]}}, "a.b"), [1, 2])

    def test_value_is_dict(self):
        self.assertEqual(lookup({"a": {"b": {"c": 5}}}, "a.b"), {"c": 5})

    def test_lookup_with_spaces(self):
        obj = {"a b": {"c d": "value"}}
        self.assertEqual(lookup(obj, "a b.c d"), "value")

    def test_valid_nested_boolean_lookup(self):
        self.assertTrue(lookup({"a": {"b": {"c": True}}}, "a.b.c"))

    def test_integer_dict_keys(self):
        self.assertEqual(lookup({1: {2: "ok"}}, "1.2"), "ok")

    def test_empty_string_key(self):
        self.assertEqual(lookup({"": {"": "empty"}}, "."), "empty")

    def test_path_with_leading_trailing_spaces(self):
        obj = {" a ": {" b ": "value"}}
        self.assertEqual(lookup(obj, " a . b "), "value")

    def test_deep_integer_keys_as_mixed_types(self):
        self.assertEqual(lookup({0: {"1": {2: "deep"}}}, "0.1.2"), "deep")

    def test_key_with_dot_in_name(self):
        self.assertEqual(lookup({"a.b": {"c": "value"}}, "a.b.c"), None)  # Because "a.b" is not a real path

    # === Realistic JSON Structures ===

    def test_realistic_json_data(self):
        obj = {
            "user": {
                "details": {"name": "Jane", "age": 30},
                "active": True
            }
        }
        self.assertEqual(lookup(obj, "user.details.name"), "Jane")
        self.assertEqual(lookup(obj, "user.details.age"), 30)
        self.assertTrue(lookup(obj, "user.active"))
        self.assertIsNone(lookup(obj, "user.status"))

    # === Invalid Lookups and Edge Cases ===

    def test_invalid_top_level_key(self):
        self.assertIsNone(lookup({"a": "b"}, "x"))

    def test_invalid_nested_key(self):
        self.assertIsNone(lookup({"a": {"b": "c"}}, "a.x"))

    def test_partial_path_break(self):
        self.assertIsNone(lookup({"a": {"b": 5}}, "a.b.c"))

    def test_path_empty_string(self):
        self.assertIsNone(lookup({"a": 1}, ""))

    def test_value_is_none(self):
        self.assertIsNone(lookup({"a": {"b": None}}, "a.b"))

    def test_middle_non_dict_type(self):
        self.assertIsNone(lookup({"a": "b"}, "a.b"))

    def test_lookup_numeric_string_as_key_in_list(self):
        self.assertIsNone(lookup({"a": {"b": [1, 2]}}, "a.b.0"))

    def test_invalid_path_type_safety(self):
        self.assertIsNone(lookup(None, "a.b"))

    def test_list_mid_path_should_fail(self):
        self.assertIsNone(lookup({"a": {"b": [1, 2, 3]}}, "a.b.c"))

    def test_object_is_empty(self):
        self.assertIsNone(lookup({}, "a"))

    def test_path_is_not_string(self):
        self.assertIsNone(lookup({"a": {"b": 1}}, None))
        self.assertIsNone(lookup({"a": {"b": 1}}, 123))

    def test_valid_prefix_then_invalid(self):
        self.assertIsNone(lookup({"a": {"b": 1}}, "a.b.c"))

    def test_path_with_trailing_dot(self):
        self.assertIsNone(lookup({"a": {"b": 1}}, "a.b."))

    def test_single_dot_path(self):
        self.assertIsNone(lookup({"a": 1}, "."))


if __name__ == "__main__":
    unittest.main()
