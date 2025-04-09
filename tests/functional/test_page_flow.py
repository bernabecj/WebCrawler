import unittest
import time
from flask_testing import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from website import create_app  # Make sure your create_app() returns a Flask instance

# CONSTANTS
PORT_NUMNER = 5200  # Port number for the Flask app


class WCTestingClass(TestCase):
    """
    Functional test that simulates user interaction via a browser.
    """

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        # options.add_argument("--headless")  # Optional: for headless mode
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

    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        app.config["LIVESERVER_PORT"] = PORT_NUMNER
        app.config["SERVER_NAME"] = f"localhost:{PORT_NUMNER}"
        return app

    # this function simulates a user opening the website in a browser and the elements he can see

    def test_open_page(self):
        # Start a test client to serve the app locally
        with self.app.test_request_context():
            url = f"http://{self.app.config['SERVER_NAME']}/"

        # The user opens the website in a browser
        self.browser.get(url)

        # Wait 1 seconds
        time.sleep(1)

        # The user see the title
        title_ele = self.browser.find_element(By.ID, "webpage-title")
        self.assertEqual(title_ele.text, "🐍 Web Crawler")

        # The user see the sidebar
        sidebar_ele = self.browser.find_element(By.ID, "sidebar")
        self.assertIsNotNone(sidebar_ele)

        # The user see the searchbar
        searchbar_ele = self.browser.find_element(By.ID, "searchInput")
        self.assertIsNotNone(searchbar_ele)

        # The user see at least one card
        cards = self.browser.find_elements(By.CSS_SELECTOR, ".news-listings .card")
        self.assertGreater(len(cards), 0, "No cards found inside .news-listings")

        # Check if page title includes expected text
        self.assertIn("Web Crawler", self.browser.title)

    def test_filtering_less_than_five_words(self):
        # Start a test client to serve the app locally
        with self.app.test_request_context():
            url = f"http://{self.app.config['SERVER_NAME']}/"

        # The user opens the website in a browser
        self.browser.get(url)

        # Wait 1 seconds
        time.sleep(1)

        searchbar_ele = self.browser.find_element(By.ID, "searchInput")

        # # Simulate typing into the search bar
        searchbar_ele.clear()
        searchbar_ele.send_keys("g")

        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".news-listings .card")
            )
        )
        cards = self.browser.find_elements(By.CSS_SELECTOR, ".news-listings .card")
        visible_cards = [card for card in cards if card.is_displayed()]

        if len(cards) > 0:
            points_list = []

            for card in visible_cards:
                # Find the element containing the points (adjust the selector if needed)
                points_text = card.find_element(
                    By.CSS_SELECTOR, ".points"
                ).text  # e.g., "24 points"
                points = int(
                    points_text.strip().split()[0]
                )  # Extract number from "24 points"
                points_list.append(points)

            # Check if points are in descending order
            if len(points_list) > 1:
                is_descending = all(
                    earlier >= later
                    for earlier, later in zip(points_list, points_list[1:])
                )
                self.assertTrue(
                    is_descending, "Points are not in descending order after filtering"
                )
        time.sleep(1)

    def test_filtering_more_than_five_words(self):
        # Start a test client to serve the app locally
        with self.app.test_request_context():
            url = f"http://{self.app.config['SERVER_NAME']}/"

        # The user opens the website in a browser
        self.browser.get(url)

        # Wait 1 seconds
        time.sleep(1)

        searchbar_ele = self.browser.find_element(By.ID, "searchInput")

        # # Simulate typing into the search bar
        searchbar_ele.clear()
        searchbar_ele.send_keys("g s f a e s")

        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".news-listings .card")
            )
        )
        cards = self.browser.find_elements(By.CSS_SELECTOR, ".news-listings .card")
        visible_cards = [card for card in cards if card.is_displayed()]

        if len(cards) > 0:
            comments_list = []

            for card in visible_cards:
                # Find the element containing the comments (adjust the selector if needed)
                comments_text = card.find_element(
                    By.CSS_SELECTOR, ".tag-comments"
                ).text  # e.g., "24 comments"
                comments = int(
                    comments_text.strip().split()[0]
                )  # Extract number from "24 points"
                comments_list.append(comments)

            # Check if points are in descending order
            if len(comments_list) > 1:
                is_descending = all(
                    earlier >= later
                    for earlier, later in zip(comments_list, comments_list[1:])
                )
                self.assertTrue(
                    is_descending, "Points are not in descending order after filtering"
                )
        time.sleep(1)
