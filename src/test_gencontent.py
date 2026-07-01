import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        result = extract_title("# Some Title")
        self.assertEqual(result, "Some Title")

    def test_no_title_raises(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass

    def test_eq_double(self):
        result = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(result, "This is a title")

    def test_eq_long(self):
        result = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(result, "title")

if __name__ == "__main__":
    unittest.main()