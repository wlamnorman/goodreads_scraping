# Goodreads scraping and reviews analysis

## How-to: `scraper.py`:
Navigate to `https://www.goodreads.com/` and click `My Books` (you probably need to have an account and be logged in). You should now be at an URL like `https://www.goodreads.com/review/list/54144458?ref=nav_mybooks`. Here The number `54144458` is your `GOODREADS_REVIEW_LIST_NUMBER`. Now simply run the script and it will output a dataframe with information about your reviews which can be analyzed.


## To-do:
- Add the following to scraping:
    * Author
    * Date reviewed
    * Date added
    * Number of reviews

- Scrape books that I have not yet read to compare my read books against "other books"