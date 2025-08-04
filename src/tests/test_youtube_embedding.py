import unittest
from markdownblock import markdown_to_html_node


class TestYoutubeEmbedding(unittest.TestCase):

    def test_youtube_watch_url(self):
        markdown = "@[youtube](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
        expected = '<div><p><iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" allowfullscreen></iframe></p></div>'
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected)

    def test_youtube_direct_embed_url(self):
        markdown = "@[youtube](https://www.youtube.com/embed/dQw4w9WgXcQ)"
        expected = '<div><p><iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" allowfullscreen></iframe></p></div>'
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected)


if __name__ == "__main__":
    unittest.main()
