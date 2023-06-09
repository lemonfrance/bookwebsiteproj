import csv
from pathlib import Path
from datetime import date, datetime
from typing import List, Dict

from bisect import insort_left

from werkzeug.security import generate_password_hash

from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import Book, Author, Publisher, Review, User, Shelf, make_review, make_shelf_association
from library.adapters.jsondatareader import BooksJSONReader, AuthorsJSONReader

repo_instance = None


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__books: List[Book] = list()
        self.__authors: List[Author] = list()
        self.__users: List[User] = list()
        self.__shelves: List[Shelf] = list()
        self.__book_reviews: List[Review] = list()

        self.__books_by_rating: List[Book] = list()
        self.__authors_by_rating: List[Author] = list()

    # Book methods
    def add_book(self, book: Book):
        self.__books.append(book)
        insort_left(self.__books_by_rating, book)

    def get_all_books(self) -> List[Book]:
        return self.__books

    def get_book_by_id(self, book_id: int):
        for b in self.__books:
            if b.book_id == book_id:
                return b
        return None

    def get_publisher_by_book_id(self, book_id: int) -> Publisher:
        for b in self.__books:
            if b.book_id == book_id:
                return b.publisher
        return None

    def get_books_by_target_year(self, target_year: int) -> List[Book]:
        return [b for b in self.__books if b.release_year == target_year]

    def get_number_of_books(self) -> int:
        return len(self.__books)

    def get_first_book(self) -> Book:
        return self.__books[0]

    def get_last_book(self) -> Book:
        return self.__books[-1]

    def get_shelf_by_name(self, shelf_name) -> Shelf:
        return next((shelf for shelf in self.__shelves if shelf.name == shelf_name), None)

    def get_all_shelves(self) -> List[Shelf]:
        return self.__shelves

    def get_books_by_author(self, author: Author) -> List[Book]:
        books_by_author = []
        for book in self.__books:
            if author in book.authors:
                books_by_author += [book]
        return books_by_author

    # Author methods
    def get_all_authors(self) -> List[Author]:
        return self.__authors;

    def add_author(self, author: Author):
        self.__authors.append(author)
        insort_left(self.__authors_by_rating, author)

    def get_author_by_id(self, author_id: int) -> Author:
        for a in self.__authors:
            if a.unique_id == author_id:
                return a

    # average rating ranking
    def get_books_by_ave_rating(self) -> List[Book]:
        return self.__books_by_rating

    def get_authors_by_ave_rating(self) -> List[Author]:
        return self.__authors_by_rating

    def get_shelves_by_ave_rating(self) -> List[Shelf]:
        return sorted(self.get_all_shelves())

    def get_books_by_year(self) -> List[Book]:
        all_books = self.__books
        sorted_books_by_year = []
        books_by_year = dict()
        for b in all_books:
            if b.release_year is not None:
                try:
                    books_by_year[b.release_year] += [b]
                except KeyError:
                    books_by_year[b.release_year] = [b]
        sorted_book_lists = list(dict(sorted(books_by_year.items())).values())
        for b_list in sorted_book_lists:
            sorted_books_by_year += b_list
        return sorted_books_by_year

    # Review methods
    def add_book_review(self, review: Review):
        super().add_book_review(review)
        self.__book_reviews += [review]

    def get_book_reviews(self, book: Book) -> List[Review]:
        return [r for r in self.__book_reviews if book.book_id == r.book.book_id]

    def get_user_reviews(self, user: User) -> List[Review]:
        return [u for u in self.__book_reviews if user.user_name == u.user.user_name]

    # User methods
    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    # Shelf methods
    def add_shelf(self, shelf: Shelf):
        if shelf in self.__shelves:
            i = self.__shelves.index(shelf)
            s = self.__shelves.pop(i)
            for b in s.shelved_books:
                shelf.add_book(b)
        self.__shelves.append(shelf)



# For JSON files (for books and authors)
def read_json_files(data_path: Path, data_type):
    books_filename = str(data_path / "comic_books_excerpt.json")
    authors_filename = str(data_path / "book_authors_excerpt.json")
    datatype = data_type

    if datatype is Book:
        reader = BooksJSONReader(books_filename, authors_filename)
        reader.read_json_files()
        return reader.dataset_of_books
    else:  # Author
        reader = AuthorsJSONReader(books_filename, authors_filename)
        reader.read_json_files()
        return reader.dataset_of_authors


def load_book_info(data_path: Path, repo: MemoryRepository):
    book_dataset: List[Book] = read_json_files(data_path, Book)
    for book_object in book_dataset:
        # Add the Book to the repository.
        repo.add_book(book_object)


def load_author_info(data_path: Path, repo: MemoryRepository):
    author_dataset: List[Author] = read_json_files(data_path, Author)
    for author_object in author_dataset:
        # Add the Author to the repository if author has books.
        books = repo.get_books_by_author(author_object)
        if books:
            repo.add_author(author_object)


# For CSV files (for users and reviews)
def read_csv_files(filename: str):
    with open(filename, encoding='utf-8-sig') as f:
        data = csv.reader(f)
        next(data)
        for row in data:
            row = [d.strip() for d in row]
            yield row


def load_users(data_path: Path, repo: MemoryRepository):
    user_dataset = dict()

    users_filepath = str(Path(data_path) / "users.csv")
    for u in read_csv_files(users_filepath):
        user_object = User(
            user_name=u[1],
            password=generate_password_hash(u[2])
        )
        repo.add_user(user_object)
        user_dataset[u[1]] = user_object
    return user_dataset


def load_reviews(data_path: Path, repo: MemoryRepository):
    reviews_fpath = str(Path(data_path) / "user_reviews.csv")
    for r in read_csv_files(reviews_fpath):
        reviewer_user = repo.get_user(r[1])
        reviewed_book = repo.get_book_by_id(int(r[2]))
        review_text = str(r[3])
        rating = int(r[4])
        timestamp = datetime.fromisoformat(r[5])

        review_object = make_review(reviewer_user, reviewed_book, review_text, rating, timestamp)
        repo.add_book_review(review_object)


def load_shelves(repo: MemoryRepository):
    all_books = repo.get_all_books()
    for b in all_books:
        for s in b.shelves:
            repo.add_shelf(s)


def populate(data_path: Path, repo: MemoryRepository):
    load_book_info(data_path, repo)
    load_author_info(data_path, repo)
    load_users(data_path, repo)
    load_reviews(data_path, repo)
    load_shelves(repo)
