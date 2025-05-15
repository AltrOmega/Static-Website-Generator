import unittest
from textnode import TextNode, TextType
from md_handle import *

class TestTextNode(unittest.TestCase):
    def _test_split_nodes_delimiter(self):
        test = TextNode("amogus **ballder** sus", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([test], '**', TextType.BOLD),[
            TextNode("amogus ", TextType.TEXT),
            TextNode("ballder", TextType.BOLD),
            TextNode(" sus", TextType.TEXT),
        ])

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


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()
