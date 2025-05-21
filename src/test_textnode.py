import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        tests = [
            (TextNode("This is a bold text node", TextType.BOLD), TextNode("This is a bold text node", TextType.BOLD)),
            (TextNode("This is a italic text node", TextType.ITALIC), TextNode("This is a italic text node", TextType.ITALIC)),
            (TextNode("This is a code text node", TextType.CODE), TextNode("This is a code text node", TextType.CODE)),
            (TextNode("This is a link text node", TextType.LINK, 'link'), TextNode("This is a link text node", TextType.LINK, 'link')),
            (TextNode("This is a image text node", TextType.IMAGE, 'image link'), TextNode("This is a image text node", TextType.IMAGE, 'image link'))
        ]

        for test in tests:
            self.assertEqual(test[0], test[1])



    def test_ne(self):
        tests = [
            (TextNode("This is a wrong text node", TextType.BOLD), TextNode("This is a bold text node", TextType.BOLD)),
            (TextNode("This is a italic text node", TextType.CODE), TextNode("This is a italic text node", TextType.ITALIC)),
            (TextNode("This is a code text node", TextType.CODE, 'link'), TextNode("This is a code text node", TextType.CODE)),
            (TextNode("                        ", TextType.LINK, 'link'), TextNode("This is a link text node", TextType.LINK, 'link')),
            (TextNode("This is a image text node", TextType.IMAGE, 'different link'), TextNode("This is a image text node", TextType.IMAGE, 'image link'))
        ]

        for test in tests:
            self.assertNotEqual(test[0], test[1])



    def test_repr(self):
        tests = [
            (repr(TextNode("This is a bold text node", TextType.BOLD)), "TextNode(This is a bold text node, TextType.BOLD, None)"),
            (repr(TextNode("This is a italic text node", TextType.ITALIC)), "TextNode(This is a italic text node, TextType.ITALIC, None)"),
            (repr(TextNode("This is a code text node", TextType.CODE)), "TextNode(This is a code text node, TextType.CODE, None)"),
            (repr(TextNode("This is a link text node", TextType.LINK, 'link')), "TextNode(This is a link text node, TextType.LINK, link)"),
            (repr(TextNode("This is a image text node", TextType.IMAGE, 'image link')), "TextNode(This is a image text node, TextType.IMAGE, image link)")
        ]

        for test in tests:
            self.assertEqual(test[0], test[1])



    def test_basic_textnode(self):
        tests = [
            (TextNode("This is a text node", TextType.TEXT), '', "This is a text node"),
            (TextNode("This is a bold node", TextType.BOLD), 'b', "This is a bold node"),
            (TextNode("This is a italic node", TextType.ITALIC), 'i', "This is a italic node"),
            (TextNode("This is a code node", TextType.CODE), "code", "This is a code node"),
        ]

        for test in tests:
            html_node = text_node_to_html_node(test[0])
            self.assertEqual(html_node.tag, test[1])
            self.assertEqual(html_node.value, test[2])

    
    def test_link_textnode(self):
        link_node = TextNode("This is a link node", TextType.LINK, url='some url')

        html_link_node = text_node_to_html_node(link_node)
        self.assertEqual(html_link_node.tag, 'a')
        self.assertEqual(html_link_node.value, "This is a link node")
        self.assertEqual(html_link_node.props, {'href': 'some url'})

    def test_image_textnode(self):
        image_node = TextNode("This is a image node", TextType.IMAGE, url='some url')

        html_link_node = text_node_to_html_node(image_node)
        self.assertEqual(html_link_node.tag, 'img')
        self.assertEqual(html_link_node.value, None)
        self.assertEqual(html_link_node.props,
            {'src': 'some url', 'alt': "This is a image node"})
            
    def test_extract_pattern(self):
        tests = [
            (extract_pattern("padding **ballder** __sus__more padding", TextType.BOLD), (("ballder",), 8, 19)),
            (extract_pattern("padding *ballder* _sus_more padding", TextType.ITALIC), (("ballder",), 8, 17)),
            (extract_pattern("`code`", TextType.CODE), (("code",), 0, 6)),
            (extract_pattern("__bald__", TextType.BOLD), (("bald",), 0, 8)),
            (extract_pattern("[link name](gugiel)", TextType.LINK), (("link name", "gugiel"), 0, 19)),
            (extract_pattern("![img fallback](some image link)", TextType.IMAGE), (("img fallback", "some image link"), 0, 32)),
        ]


        for test in tests:
            self.assertEqual(test[0], test[1])





    def test_split_nodes_by_type(self):
        tests = [
            ("this is **bolded** text", TextType.BOLD, [
                TextNode("this is ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is __bolded__ text", TextType.BOLD, [
                TextNode("this is ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is _italic_ text", TextType.ITALIC, [
                TextNode("this is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is `some ` `code` text", TextType.CODE, [
                TextNode("this is ", TextType.TEXT),
                TextNode("some ", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ]),
        ]

        for test in tests:
            self.assertListEqual(
                split_nodes_by_type(
                    [TextNode(test[0], TextType.TEXT)], test[1]
                    ),
                test[2]
            )

    def test_text_to_textnodes(self):
        tests = [
            ("this is **bolded** text", [
                TextNode("this is ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is __bolded__ text", [
                TextNode("this is ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is _italic_ text", [
                TextNode("this is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is `some ` `code` text", [
                TextNode("this is ", TextType.TEXT),
                TextNode("some ", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ]),
            ("this is `some code` and **bold** text", [
                TextNode("this is ", TextType.TEXT),
                TextNode("some code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]),
        ]

        for test in tests:
            self.assertListEqual(
                text_to_textnodes( test[0] ),
                test[1]
            )



if __name__ == "__main__":
    if 'unittest.util' in __import__('sys').modules:
        # Show full diff in self.assertEqual.
        __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

    unittest.TestCase.maxDiff = None
    unittest.main(verbosity=2)
