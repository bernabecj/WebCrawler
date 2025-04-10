# === Imports and Setup ===
import os
import unittest
from unittest.mock import patch
from flask import Flask
from website.main import views

# === Mock HTML Content for Testing ===
MOCK_HTML = """
<html>
  <body>
    <tr class="athing submission">
      <td align="right" valign="top" class="title"><span class="rank">1.</span></td>
      <td class="title">
        <a href="https://example.com">Example Title</a>
        <span class="sitestr">example.com</span>
      </td>
    </tr>
    <tr>
      <td colspan="2"></td>
      <td class="subtext">
        <span class="subline">
          <span class="score">123 points</span>
          <a href="#">42 comments</a>
        </span>
      </td>
    </tr>
  </body>
</html>
"""


# === Unit Test Class for the Index View ===
class TestIndexView(unittest.TestCase):
    def setUp(self):
        # === Set up Flask test app and route ===
        template_dir = os.path.abspath("website/templates")
        self.app = Flask(__name__, template_folder=template_dir)
        self.app.add_url_rule("/", view_func=views.Index.as_view("index"))
        self.client = self.app.test_client()

    @patch("website.main.views.requests.get")
    def test_index_view(self, mock_get):
        # === Mock external HTTP request to return test HTML ===
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = MOCK_HTML

        # === Make request to Flask route ===
        response = self.client.get("/")

        # === Validate response contains expected content ===
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Example Title", response.data)
        self.assertIn(b"123 points", response.data)
        self.assertIn(b"42 comments", response.data)


# === Run the unit tests ===
if __name__ == "__main__":
    unittest.main()
