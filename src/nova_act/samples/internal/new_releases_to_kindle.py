"""Find the latest sci-fi releases from Tor Publishing and send samples to your Kindle library.

Requires specifying a user_data_dir for a browser that is logged in to Amazon.com
See README for how to set this up.

Usage:
python -m nova_act.samples.new_releases_to_kindle [--headless]
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

import fire  # type: ignore
from pydantic import BaseModel

from nova_act import ActResult, NovaAct


class Book(BaseModel):
    title: str
    author: str


class BookList(BaseModel):
    books: list[Book]


def add_book_sample(book: Book, user_data_dir: str, headless: bool) -> ActResult:
    with NovaAct(
        starting_page="https://amazon.com",
        headless=headless,
        user_data_dir=user_data_dir,
    ) as client:
        result = client.act(
            f"Search for '{book.title} by {book.author} Kindle'. "
            "On the search results page, click that book to go to the book details page. "
            "On the book details page, if the Kindle edition is not selected, click Kindle in the box on the right. "
            "On the book details page forthe Kindle edition, click 'Send a free sample'. You may need to scroll down."
        )
        return result


def main(user_data_dir: str, headless: bool = False):
    with NovaAct(
        starting_page="https://torpublishinggroup.com/genre/science-fiction/new-releases",
        headless=headless,
    ) as client:
        result = client.act("Return the currently visible list of books", schema=BookList.model_json_schema())
        if not result.matches_schema:
            print(f"Invalid JSON {result=}")
            return
        book_list: BookList = BookList.model_validate(result.parsed_response)

        print(f"Found books: {book_list.books}")

    with ThreadPoolExecutor() as executor:
        futures = []
        for book in book_list.books:
            futures.append(executor.submit(add_book_sample, book, user_data_dir, headless))
        for future in as_completed(futures):
            future.result()


if __name__ == "__main__":
    fire.Fire(main)
