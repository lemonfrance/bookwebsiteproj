from typing import List, Iterable

from library.adapters.repository import AbstractRepository
from library.domain.model import make_review, Book, Review, Shelf, Author


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(book_id: int, review_text: str, user_name: str, rating: float, repo: AbstractRepository):
    book = repo.get_book_by_id(int(book_id))
    if book is None:
        raise NonExistentBookException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    review = make_review(review_text, user, book, rating)
    repo.add_book_review(review)


def get_book(book_id: int, repo: AbstractRepository):
    b = repo.get_book_by_id(book_id)
    if b is None:
        raise NonExistentBookException
    return book_to_dict(b)


def get_all_books(repo: AbstractRepository):
    books = repo.get_all_books()
    return books_to_dict(books)


def get_first_book(repo: AbstractRepository):
    b = repo.get_first_book()
    return book_to_dict(b)


def get_last_book(repo: AbstractRepository):
    b = repo.get_last_book()
    return book_to_dict(b)


def get_all_shelves(repo: AbstractRepository):
    shelves = repo.get_all_shelves()
    return shelves_to_dict(shelves)


def get_shelf_data(shelf_name, repo: AbstractRepository):  # get_book_ids_for_shelf
    shelf = repo.get_shelf_by_name(shelf_name)  # -> Shelf
    s = shelf_to_dict(shelf)
    return s


def get_shelves_data(shelves, repo: AbstractRepository):
    book_ids = []
    for s in shelves:
        book_ids += [get_shelf_data(s, repo)]
    return book_ids


def get_top_n_shelves(n: int, repo: AbstractRepository):
    top_shelves: List[Shelf] = list(reversed(repo.get_shelves_by_ave_rating()))
    shelves = []
    for s in top_shelves:
        shelves += [get_shelf_data(s, repo)]
    return shelves_to_dict(shelves[:n])


def get_books_by_id(id_list, repo: AbstractRepository):
    out_books = [get_book(book_id, repo) for book_id in id_list]
    return out_books


def get_reviews_for_book(book_id, repo: AbstractRepository):
    book = repo.get_book_by_id(int(book_id))

    if book is None:
        raise NonExistentBookException

    return reviews_to_dict(book.reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def book_to_dict(book: Book):
    book_dict = {
        'book_id': book.book_id,
        'publisher': book.publisher.name,
        'release_year': book.release_year,
        'title': book.title,
        'authors': authors_to_dict(book.authors),
        'description': book.description,
        'hyperlink': book.hyperlink,
        'image_hyperlink': book.image_hyperlink,
        'reviews': reviews_to_dict(book.reviews),
        'shelves': shelves_to_dict(book.shelves)
    }
    return book_dict


def books_to_dict(books: Iterable[Book]):
    return [book_to_dict(b) for b in books]


def author_to_dict(author: Author):
    author_dict = {
        'full_name': author.full_name,
        'author_id': author.unique_id
    }
    return author_dict


def authors_to_dict(authors: Iterable[Author]):
    return [author_to_dict(au) for au in authors]


def review_to_dict(review: Review):
    review_dict = {
        'user_name': review.user.user_name,
        'book_id': review.book.book_id,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(rev) for rev in reviews]


def shelf_to_dict(shelf: Shelf):
    shelf_dict = {
        'name': shelf.name,
        'shelved_books': [book.book_id for book in shelf.shelved_books]
    }
    return shelf_dict


def shelves_to_dict(shelves: Iterable[Shelf]):
    return [shelf_to_dict(shelf) for shelf in shelves]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_book(b_dict):
    book = Book(b_dict.book_id, b_dict.title, b_dict.hyperlink, b_dict.image_hyperlink)
    # Note there's no comments or tags.
    book.release_year = b_dict.release_year
    book.description = b_dict.description
    return book
