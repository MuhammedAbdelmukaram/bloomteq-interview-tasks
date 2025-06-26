import unittest
from task2.logic import lookup  # ← import, don’t redefine


class TestLookupFunction(unittest.TestCase):

    def test_valid_single_level_lookup(self):
        self.assertEqual(lookup({"key": "value"}, "key"), "value")

    def test_valid_nested_lookup(self):
        self.assertEqual(lookup({"a": {"b": {"c": "value"}}}, "a.b.c"), "value")

    def test_invalid_top_level_key(self):
        self.assertIsNone(lookup({"a": "b"}, "x"))

    def test_invalid_nested_key(self):
        self.assertIsNone(lookup({"a": {"b": "c"}}, "a.x"))

    def test_partial_path_break(self):
        self.assertIsNone(lookup({"a": {"b": 5}}, "a.b.c"))

    def test_integer_keys_as_strings(self):
        self.assertEqual(lookup({"a": {"1": {"2": "x"}}}, "a.1.2"), "x")

    def test_integer_keys(self):
        self.assertEqual(lookup({"a": {1: {2: "value"}}}, "a.1.2"), "value")

    def test_list_in_value(self):
        self.assertEqual(lookup({"a": {"b": [1, 2]}}, "a.b"), [1, 2])

    def test_path_empty_string(self):
        self.assertIsNone(lookup({"a": 1}, ""))

    def test_value_is_none(self):
        self.assertIsNone(lookup({"a": {"b": None}}, "a.b"))

    def test_middle_non_dict_type(self):
        self.assertIsNone(lookup({"a": "b"}, "a.b"))

    def test_value_is_dict(self):
        self.assertEqual(lookup({"a": {"b": {"c": 5}}}, "a.b"), {"c": 5})

    def test_lookup_numeric_string_as_key_in_list(self):
        self.assertIsNone(lookup({"a": {"b": [1, 2]}}, "a.b.0"))

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

    def test_invalid_path_type_safety(self):
        self.assertIsNone(lookup(None, "a.b"))

    def test_object_is_empty(self):
        self.assertIsNone(lookup({}, "a"))

    def test_lookup_with_spaces(self):
        obj = {"a b": {"c d": "value"}}
        self.assertEqual(lookup(obj, "a b.c d"), "value")

    def test_path_is_not_string(self):
        self.assertIsNone(lookup({"a": {"b": 1}}, None))
        self.assertIsNone(lookup({"a": {"b": 1}}, 123))

    def test_integer_dict_keys(self):
        self.assertEqual(lookup({1: {2: "ok"}}, "1.2"), "ok")

    def test_empty_string_key(self):
        self.assertEqual(lookup({"": {"": "empty"}}, "."), "empty")

    def test_valid_prefix_then_invalid(self):
        self.assertIsNone(lookup({"a": {"b": 1}}, "a.b.c"))

    def test_path_with_trailing_dot(self):
        self.assertIsNone(lookup({"a": {"b": 1}}, "a.b."))

    def test_path_with_leading_trailing_spaces(self):
        obj = {" a ": {" b ": "value"}}
        self.assertEqual(lookup(obj, " a . b "), "value")


if __name__ == "__main__":
    unittest.main()
