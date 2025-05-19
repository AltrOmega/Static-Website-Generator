import unittest
from textnode import TextType, get_type_pattern

class TextTemp(unittest.TestCase):
    def test_temp(self):
        str_ = """
    yee
    **Ballded**
    yee
"""
        found = get_type_pattern(str_, TextType.BOLD)
        print("Found: ")
        print(found.group(1))



if __name__ == "__main__":
    unittest.main()