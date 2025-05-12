import unittest
from textnode import TextNode, TextType

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
        #TextNode(TEXT, TEXT_TYPE, URL)

        tests = [
            (repr(TextNode("This is a bold text node", TextType.BOLD)), "TextNode(This is a bold text node, TextType.BOLD, None)"),
            (repr(TextNode("This is a italic text node", TextType.ITALIC)), "TextNode(This is a italic text node, TextType.ITALIC, None)"),
            (repr(TextNode("This is a code text node", TextType.CODE)), "TextNode(This is a code text node, TextType.CODE, None)"),
            (repr(TextNode("This is a link text node", TextType.LINK, 'link')), "TextNode(This is a link text node, TextType.LINK, link)"),
            (repr(TextNode("This is a image text node", TextType.IMAGE, 'image link')), "TextNode(This is a image text node, TextType.IMAGE, image link)")
        ]

        for test in tests:
            self.assertEqual(test[0], test[1])



if __name__ == "__main__":
    unittest.main()
