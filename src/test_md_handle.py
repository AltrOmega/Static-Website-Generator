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
            ("this is `code  ` text", TextType.CODE, [
                TextNode("this is ", TextType.TEXT),
                TextNode("code  ", TextType.CODE),
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



'''
    def _test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://google.com)"
        )
        self.assertListEqual([("link", "https://google.com")], matches)



    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ]
        )

    def _test_split_images_(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ]
        )
'''
if __name__ == "__main__":
    unittest.main()
