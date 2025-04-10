# === Imports and Setup ===
import unittest
import time
from flask_testing import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from website import create_app  # Ensure create_app() returns a Flask instance

# === Constants ===
PORT_NUMNER = 5200  # Port number for the Flask app

# --- Element IDs and selectors ---
WEBPAGE_TITLE_ID = "webpage-title"
SIDEBAR_ID = "sidebar"
SEARCH_INPUT_ID = "searchInput"
NEWS_CARD_SELECTOR = ".news-listings .card"
POINTS_SELECTOR = ".points"
COMMENTS_SELECTOR = ".tag-comments"


# === Functional Test Class ===
class WCTestingClass(TestCase):
    """
    Functional tests that simulate real user interaction in a browser.
    """

    # === One-Time Browser Setup ===
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        # options.add_argument("--headless")  # Optional: enable for headless mode
        options.add_argument("--log-level=3")
        options.add_argument("window-size=2020,1280")

        cls.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        cls.browser.implicitly_wait(3)
        cls.wait = WebDriverWait(cls.browser, 10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    # === Flask App Configuration for Testing ===
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        app.config["LIVESERVER_PORT"] = PORT_NUMNER
        app.config["SERVER_NAME"] = f"localhost:{PORT_NUMNER}"
        return app

    # === Test: User Opens the Page and Sees Main Elements ===
    def test_open_page(self):
        # The user navigates to the homepage
        with self.app.test_request_context():
            url = f"http://{self.app.config['SERVER_NAME']}/"
        self.browser.get(url)
        time.sleep(1)

        # The user sees the page title
        title_ele = self.browser.find_element(By.ID, WEBPAGE_TITLE_ID)
        self.assertEqual(title_ele.text, "🐍 Web Crawler")

        # The user sees the sidebar menu
        sidebar_ele = self.browser.find_element(By.ID, SIDEBAR_ID)
        self.assertIsNotNone(sidebar_ele)

        # The user sees the search bar
        searchbar_ele = self.browser.find_element(By.ID, SEARCH_INPUT_ID)
        self.assertIsNotNone(searchbar_ele)

        # The user sees a list of news cards
        cards = self.browser.find_elements(By.CSS_SELECTOR, NEWS_CARD_SELECTOR)
        self.assertGreater(len(cards), 0, f"No cards found inside {NEWS_CARD_SELECTOR}")

        # The browser title includes the app name
        self.assertIn("Web Crawler", self.browser.title)

    # === Test: User Filters Using Less Than Five Words (Sort by Points) ===
    def test_filtering_less_than_five_words(self):
        with self.app.test_request_context():
            url = f"http://{self.app.config['SERVER_NAME']}/"
        self.browser.get(url)
        time.sleep(1)

        # The user enters a short keyword in the search bar
        searchbar_ele = self.browser.find_element(By.ID, SEARCH_INPUT_ID)
        searchbar_ele.clear()
        searchbar_ele.send_keys("g")

        # Wait for results to appear
        self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, NEWS_CARD_SELECTOR))
        )

        # The user sees a filtered list of cards
        cards = self.browser.find_elements(By.CSS_SELECTOR, NEWS_CARD_SELECTOR)
        visible_cards = [card for card in cards if card.is_displayed()]

        if len(visible_cards) > 0:
            points_list = []

            # The user checks the points on each visible card
            for card in visible_cards:
                points_text = card.find_element(By.CSS_SELECTOR, POINTS_SELECTOR).text
                points = int(points_text.strip().split()[0])
                points_list.append(points)

            # The user expects the results to be sorted by descending points
            if len(points_list) > 1:
                is_descending = all(
                    earlier >= later
                    for earlier, later in zip(points_list, points_list[1:])
                )
                self.assertTrue(
                    is_descending, "Points are not in descending order after filtering"
                )

        time.sleep(1)

    # === Test: User Filters Using More Than Five Words (Sort by Comments) ===
    def test_filtering_more_than_five_words(self):
        with self.app.test_request_context():
            url = f"http://{self.app.config['SERVER_NAME']}/"
        self.browser.get(url)
        time.sleep(1)

        # The user enters a long query in the search bar
        searchbar_ele = self.browser.find_element(By.ID, SEARCH_INPUT_ID)
        searchbar_ele.clear()
        searchbar_ele.send_keys("g s f a e s")

        # Wait for filtered results
        self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, NEWS_CARD_SELECTOR))
        )

        # The user sees updated list of cards
        cards = self.browser.find_elements(By.CSS_SELECTOR, NEWS_CARD_SELECTOR)
        visible_cards = [card for card in cards if card.is_displayed()]

        if len(visible_cards) > 0:
            comments_list = []

            # The user reads the number of comments on each card
            for card in visible_cards:
                comments_text = card.find_element(
                    By.CSS_SELECTOR, COMMENTS_SELECTOR
                ).text
                comments = int(comments_text.strip().split()[0])
                comments_list.append(comments)

            # The user expects results to be sorted by descending comment count
            if len(comments_list) > 1:
                is_descending = all(
                    earlier >= later
                    for earlier, later in zip(comments_list, comments_list[1:])
                )
                self.assertTrue(
                    is_descending,
                    "Comments are not in descending order after filtering",
                )

        time.sleep(1)
