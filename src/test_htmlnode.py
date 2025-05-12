import unittest
from htmlnode import HTMLNode 

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        tests = [
                (HTMLNode(props={'sus': 'amongus'}).props_to_html(), 'sus="amongus"'),
                (HTMLNode(props={'sus': 'amongus', 'baller': 'ballyn'}).props_to_html(), 'sus="amongus" baller="ballyn"'),
                (HTMLNode(props={
                                'sus': 'amongus', 'baller': 'ballyn', 'misione': 'imposible'}).props_to_html(),
                                'sus="amongus" baller="ballyn" misione="imposible"'
                ),
        ]

        for test in tests:
            self.assertEqual(test[0], test[1])

if __name__ == "__main__":
    unittest.main()
