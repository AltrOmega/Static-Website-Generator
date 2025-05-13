import unittest
from textnode import TextNode, TextType
from md_handle import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        test = TextNode("amogus **ballder** sus", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([test], '**', TextType.BOLD),[
            TextNode("amogus ", TextType.TEXT),
            TextNode("ballder", TextType.BOLD),
            TextNode(" sus", TextType.TEXT),
        ])


if __name__ == "__main__":
    unittest.main()
