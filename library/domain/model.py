from datetime import datetime
from typing import List, Iterable


class Publisher:
    def __init__(self, publisher_name: str):
        # This makes sure the setter is called here in the initializer/constructor as well.
        self.name = publisher_name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, publisher_name: str):
        self.__name = "N/A"
        if isinstance(publisher_name, str):
            # Make sure leading and trailing whitespace is removed.
            publisher_name = publisher_name.strip()
            if publisher_name != "":
                self.__name = publisher_name

    def __repr__(self):
        return f'<Publisher {self.name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.name == self.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)


class Author:

    def __init__(self, author_id: int, author_full_name: str):
        if not isinstance(author_id, int):
            raise ValueError

        if author_id < 0:
            raise ValueError

        self.__unique_id = author_id

        # Uses the attribute setter method.
        self.full_name = author_full_name

        self.__ave_rating = 0

        # Initialize author colleagues data structure with empty set.
        # We use a set so each unique author is only represented once.
        self.__authors_this_one_has_worked_with = set()

    @property
    def unique_id(self) -> int:
        return self.__unique_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, author_full_name: str):
        if isinstance(author_full_name, str):
            # make sure leading and trailing whitespace is removed
            author_full_name = author_full_name.strip()
            if author_full_name != "":
                self.__full_name = author_full_name
            else:
                raise ValueError
        else:
            raise ValueError

    @property
    def ave_rating(self) -> float:
        return self.__ave_rating

    @ave_rating.setter
    def ave_rating(self, rating: float):
        self.__ave_rating = rating

    def add_coauthor(self, coauthor):
        if isinstance(coauthor, self.__class__) and coauthor.unique_id != self.unique_id:
            self.__authors_this_one_has_worked_with.add(coauthor)

    def check_if_this_author_coauthored_with(self, author):
        return author in self.__authors_this_one_has_worked_with

    def __repr__(self):
        return f'<Author {self.full_name}, author id = {self.unique_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.unique_id == other.unique_id

    def __lt__(self, other):
        return self.__ave_rating < other.__ave_rating

    def __hash__(self):
        return hash(self.unique_id)


class Book:

    def __init__(self, book_id: int, book_title: str, hyperlink: str, image_hyperlink: str):
        if not isinstance(book_id, int):
            raise ValueError

        if book_id < 0:
            raise ValueError

        self.__book_id = book_id

        # use the attribute setter
        self.title = book_title
        self.__description = None
        self.__publisher = None
        self.__authors = []
        self.__release_year = None
        self.__ebook = None
        self.__num_pages = None
        self.__ave_rating = 0
        self.__hyperlink: str = hyperlink
        self.__image_hyperlink: str = image_hyperlink
        self.__shelves: List[Shelf] = list()
        self.__reviews: List[Review] = list()

    @property
    def book_id(self) -> int:
        return self.__book_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, book_title: str):
        if isinstance(book_title, str):
            book_title = book_title.strip()
            if book_title != "":
                self.__title = book_title
            else:
                raise ValueError
        else:
            raise ValueError

    @property
    def ave_rating(self) -> float:
        return self.__ave_rating

    @ave_rating.setter
    def ave_rating(self, rating: float):
        self.__ave_rating = rating

    @property
    def hyperlink(self) -> str:
        return self.__hyperlink

    @property
    def image_hyperlink(self) -> str:
        return self.__image_hyperlink

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, release_year: int):
        if isinstance(release_year, int) and release_year >= 0:
            self.__release_year = release_year
        else:
            raise ValueError

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str):
            self.__description = description.strip()

    @property
    def publisher(self) -> Publisher:
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            self.__publisher = publisher
        else:
            self.__publisher = None

    @property
    def authors(self) -> List[Author]:
        return self.__authors

    def add_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            return

        self.__authors.append(author)

    def remove_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            self.__authors.remove(author)

    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self.__reviews)

    def add_review(self, review: 'Review'):
        self.__reviews.append(review)

    @property
    def shelves(self) -> List['Shelf']:
        return self.__shelves

    def is_shelved_by(self, s: 'Shelf'):
        return s in self.__shelves

    def is_shelved(self) -> bool:
        return len(self.__shelves) > 0

    def add_shelf(self, shelf: 'Shelf'):
        self.__shelves.append(shelf)

    @property
    def ebook(self) -> bool:
        return self.__ebook

    @ebook.setter
    def ebook(self, is_ebook: bool):
        if isinstance(is_ebook, bool):
            self.__ebook = is_ebook

    @property
    def num_pages(self) -> int:
        return self.__num_pages

    @num_pages.setter
    def num_pages(self, num_pages: int):
        if isinstance(num_pages, int) and num_pages >= 0:
            self.__num_pages = num_pages

    def __repr__(self):
        return f'<Book {self.title}, book id = {self.book_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.book_id == other.book_id

    def __lt__(self, other):
        return self.__ave_rating < other.__ave_rating

    def __hash__(self):
        return hash(self.book_id)


class Shelf:
    def __init__(self, shelf_name: str):
        self.__name: str = shelf_name
        self.__shelved_books: List[Book] = list()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def shelved_books(self) -> List[Book]:
        return self.__shelved_books

    def number_of_shelved_books(self) -> int:
        return len(self.__shelved_books)

    def contains(self, book: Book) -> bool:
        return book in self.__shelved_books

    def add_book(self, book: Book):
        self.__shelved_books.append(book)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name

    def __lt__(self, other):
        this_shelf_rating = 0
        other_shelf_rating = 0
        for ssb in self.shelved_books:
            this_shelf_rating += ssb.ave_rating
        for osb in other.shelved_books:
            other_shelf_rating += osb.ave_rating
        this_shelf_rating = this_shelf_rating/(self.number_of_shelved_books()*5)
        other_shelf_rating = other_shelf_rating/(other.number_of_shelved_books()*5)
        return this_shelf_rating < other_shelf_rating


class Review:
    def __init__(self, user: 'User', book: Book, review_text: str, rating: int):
        self.__user = user

        if isinstance(book, Book):
            self.__book = book
        else:
            self.__book = None

        if isinstance(review_text, str):
            self.__review_text = review_text.strip()
        else:
            self.__review_text = "N/A"

        if isinstance(rating, int) and 1 <= rating <= 5:
            self.__rating = rating
        else:
            raise ValueError

        self.__timestamp = datetime.now()

    @property
    def user(self) -> 'User':
        return self.__user

    @property
    def book(self) -> Book:
        return self.__book

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return other.user == self.user and other.book == self.book and other.review_text == self.review_text \
            and other.rating == self.rating and other.timestamp == self.timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __repr__(self):
        return f'<Review of book {self.book}, rating = {self.rating}, timestamp = {self.timestamp}>'


class User:
    def __init__(self, user_id: int, user_name: str, password: str):
        if user_name == "" or not isinstance(user_name, str):
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()

        if password == "" or not isinstance(password, str) or len(password) < 7:
            self.__password = None
        else:
            self.__password = password

        self.__user_id = user_id
        self.__read_books = []
        self.__reviews = []
        self.__pages_read = 0

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def read_books(self) -> List[Book]:
        return self.__read_books

    @property
    def reviews(self) -> List[Review]:
        return self.__reviews

    @property
    def pages_read(self) -> int:
        return self.__pages_read

    def read_a_book(self, book: Book):
        if isinstance(book, Book):
            self.__read_books.append(book)
            if book.num_pages is not None:
                self.__pages_read += book.num_pages

    def add_review(self, review: Review):
        if isinstance(review, Review):
            # Review objects are in practice always considered different due to their timestamp.
            self.__reviews.append(review)

    def has_reviewed(self, book: Book):
        r: Review
        for r in self.__reviews:
            if r.user == self.__user_id and r.book == book.book_id:
                return True
        return False

    def __repr__(self):
        return f'<User {self.user_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user_name == self.user_name

    def __lt__(self, other):
        return self.user_name < other.user_name

    def __hash__(self):
        return hash(self.user_name)


class BooksInventory:

    def __init__(self):
        self.__books = {}
        self.__prices = {}
        self.__stock_count = {}

    def add_book(self, book: Book, price: int, nr_books_in_stock: int):
        self.__books[book.book_id] = book
        self.__prices[book.book_id] = price
        self.__stock_count[book.book_id] = nr_books_in_stock

    def remove_book(self, book_id: int):
        self.__books.pop(book_id)
        self.__prices.pop(book_id)
        self.__stock_count.pop(book_id)

    def find_book(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__books[book_id]
        return None

    def find_price(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__prices[book_id]
        return None

    def find_stock_count(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__stock_count[book_id]
        return None

    def search_book_by_title(self, book_title: str):
        for book_id in self.__books.keys():
            if self.__books[book_id].title == book_title:
                return self.__books[book_id]
        return None


class ModelException(Exception):
    pass


def make_review_association(r: Review, user: User, book: Book):
    # A review connects a book to a user
    # A book can only be reviewed by a user once

    if user.has_reviewed(book):
        raise ModelException(f' "{book.title}" has already been reviewed by user {user.user_name}')

    user.add_review(r)
    book.add_review(r)


def make_shelf_association(book: Book, shelf: Shelf):
    if shelf.contains(book):
        raise ModelException(f'Shelf {shelf.name} already contains Book "{book.title}"')

    book.add_shelf(shelf)
    shelf.add_book(book)
