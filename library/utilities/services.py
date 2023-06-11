from typing import Iterable
import random

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Author, Shelf, Review, User


def get_year_sorted_books(repo: AbstractRepository):
    year_sorted_books = repo.get_books_by_year()
    return books_to_dict(year_sorted_books)


def get_ranked_books(repo: AbstractRepository):
    ranked_books = repo.get_books_by_ave_rating()
    return books_to_dict(ranked_books)


def get_ranked_authors(repo: AbstractRepository):
    ranked_authors = repo.get_authors_by_ave_rating()
    return authors_to_dict(ranked_authors)


def get_shelf_names(repo: AbstractRepository):
    shelves = repo.get_all_shelves()
    shelf_names = [s.name for s in shelves]
    return shelf_names


def get_book_ids(repo: AbstractRepository):
    books = repo.get_all_books()
    book_ids = [b.book_id for b in books]
    return book_ids


def get_random_n_shelves(n: int, repo: AbstractRepository):
    shelf_count: int = len(repo.get_all_shelves())
    if n >= shelf_count:
        n = shelf_count - 1

    # Pick distinct and random shelves.
    # random_indexes = random.sample(range(1, shelf_count), n)
    random_indexes = []
    for i in range(0, n):
        random_indexes += [random.choice(range(0, shelf_count))]
    all_shelves = repo.get_all_shelves()
    random_shelves = []
    for ri in random_indexes:
        random_shelves += [all_shelves[ri]]
    return shelves_to_dict(random_shelves)


def get_user_reviews(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    user_reviews = repo.get_user_reviews(user)
    return reviews_to_dict(user_reviews)


# ============================================
# Functions to convert dicts to model entities
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
        'image_hyperlink': book.image_hyperlink
    }
    return book_dict


def books_to_dict(books: Iterable[Book]):
    return [book_to_dict(book) for book in books]


def shelf_to_dict(shelf: Shelf):
    shelf_dict = {
        'name': shelf.name,
        'shelved_books': [book.book_id for book in shelf.shelved_books]
    }
    return shelf_dict


def shelves_to_dict(shelves: Iterable[Shelf]):
    return [shelf_to_dict(shelf) for shelf in shelves]


def author_to_dict(author: Author):
    if author.full_name != None:
        author_dict = {
            'full_name': author.full_name,
            'author_id': author.unique_id
        }
        return author_dict


def authors_to_dict(authors: Iterable[Author]):
    return [author_to_dict(au) for au in authors]


def review_to_dict(review: Review):
    review_dict = {
        'book': review.book,
        'user': review.user,
        'rating': review.rating,
        'review_text': review.review_text,
        # 'timestamp': review.timestamp
        'timestamp': 0
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(r) for r in reviews]
