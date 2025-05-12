import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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



    def test_to_html_with_children(self):
        tests = [
            (ParentNode("div", [LeafNode("span", "child")]) ,"<div><span>child</span></div>"),
            (ParentNode("div", [LeafNode("h1", "amogus")]) ,"<div><h1>amogus</h1></div>"),
            (ParentNode("a", [LeafNode("span", "baller")]) ,"<a><span>baller</span></a>"),
            (ParentNode("div", [
                LeafNode("span", "child"),
                LeafNode("span", "baller"),
                LeafNode("h1", "amogus")
            ]), "<div><span>child</span><span>baller</span><h1>amogus</h1></div>"),
        ]

        for test in tests:
            self.assertEqual(test[0].to_html(), test[1])

    def test_to_html_with_grandchildren(self):
        tests = [
            (ParentNode("div",[
                    ParentNode("span", [
                        LeafNode("b", "grandchild")])
            ]), "<div><span><b>grandchild</b></span></div>"),

            (ParentNode("div",[
                    ParentNode("span", [
                        LeafNode("b", "grandchild_1")]),
                    ParentNode("span", [
                        LeafNode("b", "grandchild_2")])
            ]), "<div><span><b>grandchild_1</b></span><span><b>grandchild_2</b></span></div>"),

            (ParentNode("h1",[
                    ParentNode("div", [
                        LeafNode("a", "grandchild_1")]),
                    ParentNode("span", [
                        LeafNode("b", "grandchild_2")])
            ]), "<h1><div><a>grandchild_1</a></div><span><b>grandchild_2</b></span></h1>"),
        ]


        for test in tests:
            self.assertEqual(test[0].to_html(), test[1])


if __name__ == "__main__":
    unittest.main()
