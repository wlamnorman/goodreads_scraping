import requests
import time
from bs4 import BeautifulSoup
import logging
import pandas as pd
from parsing_utilities import parse_scraped_reviews

GOODREADS_REVIEW_LIST_NUMBER: int = 54144458


def main():
    initialize_logger()
    scraped_webpages = scrape_webpage_paginate(GOODREADS_REVIEW_LIST_NUMBER)
    reviews = parse_scraped_reviews(scraped_webpages)
    save_dataframe_to_pickle(reviews, "reviews_dataframe")


def scrape_webpage(url: str) -> bytes | None:
    """
    Fetches the content of a webpage.

    Parameters:
        url (str): The URL of the webpage to scrape.

    Returns:
        bytes | None: The raw content of the webpage if successful, None otherwise.
    """
    try:
        logging.info(f"Attempting to fetch content from {url}")
        page = requests.get(url)
        page.raise_for_status()
        logging.info(f"Successfully fetched content from {url}")
        return page.content
    except requests.exceptions.HTTPError as e:
        logging.error(f"An error occurred while fetching content from {url}: {e}")


def scrape_webpage_paginate(
    review_list_number: int, sec_sleep_between_scraping: float = 2
) -> list[bytes]:
    def has_content(page_content: bytes) -> bool:
        soup = BeautifulSoup(page_content, "html.parser")
        if soup.find("div", {"class": "greyText nocontent stacked"}):
            return False
        return True

    scraped_webpages = []
    page_number = 1
    while True:
        url = f"https://www.goodreads.com/review/list/{review_list_number}?page={page_number}"
        page_content = scrape_webpage(url)

        if not has_content(page_content):
            logging.info(
                f"Scraping is done as no more content could be found after scraping {page_number} pages."
            )
            break

        scraped_webpages.append(page_content)

        time.sleep(sec_sleep_between_scraping)
        page_number += 1
    return scraped_webpages


def save_dataframe_to_pickle(df: pd.DataFrame, save_name: str) -> None:
    try:
        df.to_pickle(f"{save_name}.pickle")
        logging.info(f"Successfully saved DataFrame to {save_name}.pickle.")
    except Exception as e:
        logging.error(f"An error occurred while saving the DataFrame: {e}")


def initialize_logger():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info(f"Scraping reviews from the requested Goodreads list of reviews.")


if __name__ == "__main__":
    main()
