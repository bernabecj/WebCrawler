import requests
from bs4 import BeautifulSoup
from flask import render_template
from flask.views import View

# CONSTANTS
PAGE_URL = "https://news.ycombinator.com/"


class Index(View):
    template = "index.html"

    def dispatch_request(self):
        # Scraping Hacker News
        response = requests.get(PAGE_URL)
        soup = BeautifulSoup(response.text, "html.parser")

        items = []

        for tr in soup.find_all("tr", class_="athing submission"):
            # Extract the rank number
            rank_span = tr.find("span", class_="rank")
            rank = rank_span.text.strip().rstrip(".") if rank_span else None

            # Extract the title and link
            title_td = tr.find_all("td", class_="title")[1]
            link_tag = title_td.find("a") if title_td else None

            title = link_tag.text.strip() if link_tag else None
            link = link_tag.get("href") if link_tag else None

            # Extract site name
            site_tag = title_td.find("span", class_="sitestr")
            site_name = site_tag.text.strip() if site_tag else None

            # Move to the next row to extract points and comments
            subtext_tr = tr.find_next_sibling("tr")
            subline = subtext_tr.find("span", class_="subline") if subtext_tr else None

            # Extract points
            score_span = subline.find("span", class_="score") if subline else None
            points = "0"
            if score_span:
                points_text = score_span.text.strip()
                points = points_text.split()[0]

            # Extract comments (numeric only)
            comments = "0"
            if subline:
                comment_links = subline.find_all("a")
                if comment_links:
                    last_link = comment_links[-1]
                    if "comment" in last_link.text:
                        comments_text = last_link.text.strip()
                        comments = comments_text.split()[0]

            # Append the scraped data
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

        print(items[0])
        return render_template(self.template, items=items)
