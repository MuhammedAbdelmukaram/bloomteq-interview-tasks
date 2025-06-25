import unittest
from task1.logic import generate_new_entry


class TestGenerateNewEntry(unittest.TestCase):

    # --- Typical Cases ---

    # Empty case should just initialize it at 1,1
    def test_empty_list(self):
        self.assertEqual(generate_new_entry([]), {"id": 1, "value": 1})

    # Basic working case from PDF
    def test_basic_case(self):
        data = [
            {"id": 1, "value": 3},
            {"id": 2, "value": 7},
            {"id": 3, "value": 3},
            {"id": 4, "value": 1},
            {"id": 5, "value": 4},
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 6, "value": 5})

    # Basic case, but allowed value repeats three times
    def test_basic_case_with_triple_repetition(self):
        data = [
            {"id": 1, "value": 3},
            {"id": 2, "value": 7},
            {"id": 3, "value": 3},
            {"id": 4, "value": 1},
            {"id": 5, "value": 4},
            {"id": 6, "value": 3},
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 7, "value": 5})

    # Basic case, but there are
    def test_basic_case_with_triple_repetition_and_smaller_double_repetition(self):
        data = [
            {"id": 1, "value": 3},
            {"id": 2, "value": 7},
            {"id": 3, "value": 3},
            {"id": 4, "value": 1},
            {"id": 5, "value": 4},
            {"id": 6, "value": 3},
            {"id": 7, "value": 2},
            {"id": 8, "value": 2},
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 9, "value": 5})

    # the way it should be handled is, the second duplicate ID is to be ignored
    # this however depends on requirements so I would ask further for clarification
    # in real situation
    def test_duplicate_ids(self):
        data = [
            {"id": 1, "value": 3},
            {"id": 1, "value": 9},
            {"id": 2, "value": 3},
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 3, "value": 4})

    # Test where I check does it make any difference if we only have 2 values
    # And both are the same
    def test_repeated_value_only(self):
        data = [
            {"id": 1, "value": 5},
            {"id": 2, "value": 5}
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 3, "value": 6})

    # --- Edge & Error Cases ---

    # If no value is duplicate, it should return "None"
    def test_no_value_used_twice(self):
        data = [
            {"id": 1, "value": 1},
            {"id": 2, "value": 2},
            {"id": 3, "value": 3},
        ]
        result = generate_new_entry(data)
        self.assertIsNone(result)

    # In case we have invalid entries, we should only consider the valid ones
    # Of course, this would further be checked for clarification concerning handling
    # But in my implementation, I will consider, and not throw exception
    def test_invalid_entries(self):
        data = [
            {"id": 1, "value": 3},
            {"value": 3},  # missing 'id'
            {"id": 2, "value": "bad"},  # non-int value
            "not a dict",  # completely invalid
            {"id": None, "value": 2},
            {"id": 3, "value": None},
        ]
        result = generate_new_entry(data)
        self.assertIsNone(result)  # only 1 valid entry

    # Testing negative values, and their impact, given that there is positive duplicate
    def test_negative_values(self):
        data = [
            {"id": 1, "value": -1},
            {"id": 2, "value": -1},
            {"id": 3, "value": 1},
            {"id": 4, "value": 1},
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 5, "value": 2})  # 1 repeated, 2 next positive

    # Testing basically basic case, but with small caveat which is the gap
    def test_repeated_low_value_and_all_others_gap(self):
        data = [
            {"id": 1, "value": 1},
            {"id": 2, "value": 1},
            {"id": 3, "value": 10},
            {"id": 4, "value": 11},
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 5, "value": 2})  # 1 is repeated, 2 is next missing

    # Testing larger gaps. I don't expect this to make any difference, its a
    # "good to have" type of test
    def test_large_gap_and_high_values(self):
        data = [
            {"id": 1, "value": 100000},
            {"id": 2, "value": 100000},
            {"id": 3, "value": 100000},
            {"id": 4, "value": 100000},
            {"id": 5, "value": 2},
            {"id": 6, "value": 3},
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 7, "value": 100001})  # 100 repeated, 1 is lowest missing

    # Testing sparse high values, and how they impact the result, its different
    # from the first test because expected value is smaller, and data inputs
    # go from smaller to larger as opposed to the one above
    def test_sparse_high_values_with_small_repeats(self):
        data = [
            {"id": 1, "value": 1},
            {"id": 2, "value": 1},  # repeated small value
            {"id": 3, "value": 1000},
            {"id": 4, "value": 2000},
            {"id": 5, "value": 3340},
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 6, "value": 2})  # 1 repeated, 2 is missing and valid

    # --- Large Data Sets ---

    # So 10 gets repeated 1000 times, and on top of that I am adding
    # 2 more, to see if the third will be correct (similar to test above)
    def test_large_basic_case_with_repeats(self):
        # Repeat value 10 exactly 1000 times
        data = [{"id": i + 1, "value": 10} for i in range(1000)]
        # Add some other random values
        data += [
            {"id": 1001, "value": 20},
            {"id": 1002, "value": 30}
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 1003, "value": 11})  # 10 is repeated, 11 is next missing

    # Testing 11 figure values (To be used as guidance for optimizations)
    def test_massive_sparse_values(self):
        # Add sparse values (100, 200, 300, ...)
        data = [{"id": i + 1, "value": i * 10000000000} for i in range(1, 1001)]
        # Repeat a small value at least twice
        data.append({"id": 1002, "value": 2})
        data.append({"id": 1003, "value": 2})
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 1004, "value": 3})  # 1 is missing, 2 is repeated

    # Testing even duplicates from 1 to 5001. The result should be
    # "id": 5001, "value": 3, because larger dupliactes, even with gaps
    # which provide opportunity for conditions to be met won't affect it
    def test_high_load_with_duplicates_and_gaps(self):
        # 5000 entries, every even number repeated
        data = []
        for i in range(1, 5001):
            value = i if i % 2 == 0 else i + 1  # duplicates on even values
            data.append({"id": i, "value": value})
        result = generate_new_entry(data)
        # smallest positive number not present is 1, but allowed one is 3
        # because duplicate starts from value 2
        self.assertEqual(result, {"id": 5001, "value": 3})

    # Similar to a version of smaller data set with incorrect values from above
    # At the very end I just add two more correctvalues just so I can see will
    # any of it affect the algorithm
    def test_many_invalid_entries_with_some_valid(self):
        data = [{"id": i, "value": "bad"} for i in range(1, 1000)]
        data.append({"id": 1000, "value": "not a dict"})
        data.append("not a dict")
        data.append({"id": 1000})
        # Now adding some valid repeated value
        data += [
            {"id": 1001, "value": 4},
            {"id": 1002, "value": 4}
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 1003, "value": 5})  # 1 is missing, 4 is repeated

    # Testing does having every number duplicated impact the final solution
    def test_candidate_above_multiple_repeats(self):
        data = [
            {"id": 1, "value": 1},
            {"id": 2, "value": 1},
            {"id": 3, "value": 2},
            {"id": 4, "value": 2},
            {"id": 5, "value": 3},
            {"id": 6, "value": 3},
        ]
        # 4 is missing, 1/2/3 are all repeated → 4 is valid
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 7, "value": 4})

    # Almost basic case test, but I did it as I wasnt sure about something
    # in the algorithm, just so I could use debuger and check it
    # probably unnecessary
    def test_multiple_gaps_only_one_valid(self):
        data = [
            {"id": 1, "value": 1},
            {"id": 2, "value": 1},
            {"id": 3, "value": 4},
            {"id": 4, "value": 6},
            {"id": 5, "value": 7}
        ]
        # Gaps: 2, 3, 5
        # 1 is repeated, so 2 and 3 are valid, but 2 is the smallest
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 6, "value": 2})

    # Testing negative repeated values
    # Task says to add smallest positive integer not present anywhere
    # But it never says that negative duplicate or 0 duplicates
    # are not "enablers"
    def test_negative_repeated_values(self):
        data = [
            {"id": 1, "value": -1},
            {"id": 2, "value": -1},
            {"id": 3, "value": 1},
            {"id": 4, "value": 2},
            {"id": 5, "value": 3}
        ]
        # All positive values are unique, repeated value (-1) is negative
        # So no valid positive candidate has a smaller repeated value → None
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 6, "value": 4})

    # Based on the comment from the test above, I just added 0 as a duplicate
    def test_negative_and_zero_repeated_values(self):
        data = [
            {"id": 1, "value": -1},
            {"id": 2, "value": -1},
            {"id": 3, "value": 0},
            {"id": 4, "value": 0},
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 5, "value": 1})

    def test_negative_and_zero_repeated_values_with_single_positive(self):
        data = [
            {"id": 1, "value": -1},
            {"id": 2, "value": -1},
            {"id": 3, "value": 0},
            {"id": 4, "value": 0},
            {"id": 5, "value": 1},
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 6, "value": 2})

    def test_negative_and_zero_repeated_values_with_repeated_positive(self):
        data = [
            {"id": 1, "value": -1},
            {"id": 2, "value": -1},
            {"id": 3, "value": 0},
            {"id": 4, "value": 0},
            {"id": 5, "value": 1},
            {"id": 6, "value": 1},
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 7, "value": 2})

    # True border case for the algorithm, to check will it give -4, 0, or
    # actually correct value of 1
    def test_all_negative_values_empty_positive_candidate(self):
        data = [
            {"id": 1, "value": -5},
            {"id": 2, "value": -3},
            {"id": 3, "value": -5}
        ]
        # Nothing positive → should return {"id": 4, "value": 1}
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 4, "value": 1})

    # Similar to tests above, but instead of dupliacte negative we have
    # duplicate 0
    def test_zero_and_negative_values_ignored(self):
        data = [
            {"id": 1, "value": 0},
            {"id": 2, "value": 0},
            {"id": 3, "value": 1},
            {"id": 4, "value": 1},
        ]
        # 0 is repeated but invalid; 1 is repeated → 2 is valid
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 5, "value": 2})

    # Border case which tends to expect 4, and not 1, so the "between" problem
    def test_single_repeated_negative_and_valid_repeated_positive(self):
        data = [
            {"id": 1, "value": -3},
            {"id": 2, "value": -3},
            {"id": 3, "value": 2},
            {"id": 4, "value": 2},
            {"id": 5, "value": 3}
        ]
        result = generate_new_entry(data)
        self.assertEqual(result, {"id": 6, "value": 1})

if __name__ == "__main__":
    unittest.main()
