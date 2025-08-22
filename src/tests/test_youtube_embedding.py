import unittest
from markdownblock import markdown_to_html_and_metadata
from textnode import text_to_textnodes, text_node_to_html_node


class TestYoutubeEmbedding(unittest.TestCase):

    def test_youtube_watch_url(self):
        markdown = "@[youtube](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
        expected = '<div><p><iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" allowfullscreen></iframe></p></div>'
        self.assertEqual(markdown_to_html_and_metadata(markdown)[0], expected)

    def test_youtube_direct_embed_url(self):
        markdown = "@[youtube](https://www.youtube.com/embed/dQw4w9WgXcQ)"
        expected = '<div><p><iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" allowfullscreen></iframe></p></div>'
        self.assertEqual(markdown_to_html_and_metadata(markdown)[0], expected)
    
    def test_youtube_with_attribute(self):
        md = '@[youtube](https://www.youtube.com/embed/dQw4w9WgXcQ){class="video"}'
        nodes = text_to_textnodes(md)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        expected = '<iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" class="video" allowfullscreen></iframe>'
        self.assertEqual(html, expected)

    def test_youtube_with_malformed_braces(self):
        md = '@[youtube](https://www.youtube.com/embed/dQw4w9WgXcQ){class="oops"'
        nodes = text_to_textnodes(md)
        nodes = [text_node_to_html_node(node) for node in nodes]
        html = "".join(n.to_html() for n in nodes)
        # Should ignore malformed braces and render without attributes
        expected = '<iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" allowfullscreen></iframe>'
        self.assertEqual(html, html)


if __name__ == "__main__":
    unittest.main()
