from bs4 import BeautifulSoup, element
from collections import defaultdict
import pandas as pd


def parse_scraped_reviews(scraped_webpages: list[bytes]) -> pd.DataFrame:
    reviews: list = []
    for webpage_content in scraped_webpages:
        soup = BeautifulSoup(webpage_content, "html.parser")
        reviews_html_format = soup.find_all(class_="bookalike review")
        for review in reviews_html_format:
            review_dict = parse_review(review)
            reviews.append(review_dict)
    return pd.DataFrame.from_dict(reviews)


def parse_review(review: element.Tag) -> dict:
    return {
        "title": get_review_title(review),
        "avg_rating": get_review_average_rating(review),
        "my_rating": get_review_my_rating(review),
    }


def get_review_title(review: element.Tag) -> str:
    return review.find("td", class_="field title").find("a").text.strip()


def get_review_average_rating(review: element.Tag) -> float:
    return float(
        review.find("td", {"class": "field avg_rating"})
        .find("div", {"class": "value"})
        .text.strip()
    )


def ratings_mapping() -> defaultdict:
    ratings_mapping = defaultdict(lambda: None)
    ratings_mapping.update(
        {
            "it was amazing": 5,
            "really liked it": 4,
            "liked it": 3,
            "it was ok": 2,
            "did not like it": 1,
        }
    )
    return ratings_mapping


def get_review_my_rating(review: element.Tag) -> int:
    span_tag = review.find("span", {"class": "staticStars notranslate"})
    title_value = span_tag["title"] if "title" in span_tag.attrs else None
    return ratings_mapping()[title_value]
