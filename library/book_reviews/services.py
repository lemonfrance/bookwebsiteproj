from typing import List, Iterable

from library.adapters.repository import AbstractRepository
from library.books.services import NonExistentBookException
from library.domain.model import Book, Review, Shelf, Author


class CharacterLimitException(Exception):
    pass


def add_review(book_id: int, user_name: str, review_text: str, rating: int, repo: AbstractRepository):
    book = repo.get_book_by_id(book_id)

    repo.add_book_review(
        Review(
            user=repo.get_user(user_name),
            book=repo.get_book_by_id(book_id),
            review_text=review_text,
            rating=rating,
        )
    )


def get_reviews_for_book(book_id, repo: AbstractRepository):
    book = repo.get_book_by_id(book_id)

    if book is None:
        raise NonExistentBookException

    return reviews_to_dict(book.reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================


def book_to_dict(book: Book):
    book_dict = {
        'book_id': book.book_id,
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


def shelf_to_dict(shelf: Shelf):
    shelf_dict = {
        'name': shelf.name,
        'shelved_books': [book.book_id for book in shelf.shelved_books]
    }
    return shelf_dict


def shelves_to_dict(shelves: Iterable[Shelf]):
    return [shelf_to_dict(shelf) for shelf in shelves]


def review_to_dict(review: Review):
    review_dict = {
        'user_name': review.user.user_name,
        'book_id': review.book.book_id,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(rev) for rev in reviews]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_book(dict):
    book = Book(dict.book_id, dict.title, dict.hyperlink, dict.image_hyperlink)
    # Note there's no comments or tags.
    return book
