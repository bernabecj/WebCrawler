# === Imports ===
import requests
from bs4 import BeautifulSoup
from flask import render_template
from flask.views import View

# === Constants ===
PAGE_URL = "https://news.ycombinator.com/"  # Target URL for scraping Hacker News


# === View Class for Index Page ===
class Index(View):
    template = "index.html"  # HTML template to render

    def dispatch_request(self):
        # === Fetch HTML Content from Hacker News ===
        response = requests.get(PAGE_URL)
        soup = BeautifulSoup(response.text, "html.parser")

        items = []  # List to hold all the extracted news items

        # === Parse All News Rows ===
        for tr in soup.find_all("tr", class_="athing submission"):
            # --- Extract Rank ---
            rank_span = tr.find("span", class_="rank")
            rank = rank_span.text.strip().rstrip(".") if rank_span else None

            # --- Extract Title and Link ---
            title_td = tr.find_all("td", class_="title")[1]
            link_tag = title_td.find("a") if title_td else None
            title = link_tag.text.strip() if link_tag else None
            link = link_tag.get("href") if link_tag else None

            # --- Extract Source Site Name ---
            site_tag = title_td.find("span", class_="sitestr")
            site_name = site_tag.text.strip() if site_tag else None

            # === Move to Next Row to Extract Subtext Info (points & comments) ===
            subtext_tr = tr.find_next_sibling("tr")
            subline = subtext_tr.find("span", class_="subline") if subtext_tr else None

            # --- Extract Points ---
            score_span = subline.find("span", class_="score") if subline else None
            points = "0"
            if score_span:
                points_text = score_span.text.strip()  # e.g., "123 points"
                points = points_text.split()[0]  # Extract number only

            # --- Extract Comments ---
            comments = "0"
            if subline:
                comment_links = subline.find_all("a")
                if comment_links:
                    last_link = comment_links[-1]
                    if "comment" in last_link.text:
                        comments_text = last_link.text.strip()  # e.g., "42 comments"
                        comments = comments_text.split()[0]  # Extract number only

            # === Store Extracted Data ===
            items.append(
                {
                    "rank": rank,
                    "title": title,
                    "link": link,
                    "site": site_name,
                    "points": points,
                    "comments": comments,
                }
            )

        # === Render the Template with Parsed Items ===
        return render_template(self.template, items=items)
