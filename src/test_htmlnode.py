import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        tests = [
                (HTMLNode(props={'sus': 'amongus'}).props_to_html(), ' sus="amongus"'),
                (HTMLNode(props={'sus': 'amongus', 'baller': 'ballyn'}).props_to_html(), ' sus="amongus" baller="ballyn"'),
                (HTMLNode(props={
                                'sus': 'amongus', 'baller': 'ballyn', 'misione': 'imposible'}).props_to_html(),
                                ' sus="amongus" baller="ballyn" misione="imposible"'
                ),
        ]

        for test in tests:
            self.assertEqual(test[0], test[1])



    def test_leaf_to_html_p(self):
        tests = [
            (LeafNode("p", "Hello, world!").to_html(), "<p>Hello, world!</p>"),
            (LeafNode("h1", "SCREAMING EAGLES").to_html(), "<h1>SCREAMING EAGLES</h1>"),

            (LeafNode("a", "Google link",
                props={'href': 'https://www.google.com'}).to_html(),
                '<a href="https://www.google.com">Google link</a>'),

            (LeafNode("a", "Google link ext",
                props={'href': 'https://www.google.com', 'ext': 'VOID'}).to_html(),
                '<a href="https://www.google.com" ext="VOID">Google link ext</a>'),
        ]

        for test in tests:
            self.assertEqual(test[0], test[1])

if __name__ == "__main__":
    unittest.main()
