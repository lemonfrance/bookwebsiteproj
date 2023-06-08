from typing import List, Iterable

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Review, Shelf, Author


class NonExistentAuthorException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_author(author_id: int, repo: AbstractRepository):
    a = repo.get_author_by_id(author_id)
    if a is None:
        raise NonExistentAuthorException
    return author_to_dict(a)


def get_author_books(author_id: int, repo: AbstractRepository):
    author = get_author(author_id, repo)
    books_by_author = repo.get_books_by_author(Author(author_id,author['full_name']))
    return books_to_dict(books_by_author)


def get_all_authors(repo: AbstractRepository):
    authors = repo.get_all_authors()
    return authors_to_dict(authors)


def get_ranked_authors(repo: AbstractRepository):
    authors = repo.get_authors_by_ave_rating()
    authors=reversed(authors)
    return authors_to_dict(authors)


def search_for_author(search_string: str, repo: AbstractRepository):
    authors = get_all_authors(repo)
    search_results_fn = []
    search_results_ln = []
    search_results_bk = []
    for a in authors:
        author_name_list = a['full_name'].split()
        matches_first_name = author_name_list[0].startswith(search_string)
        matches_last_name = author_name_list[-1].startswith(search_string)
        matches_a_book_title = False
        a_books = get_author_books(a['author_id'])
        for book in a_books:
            title = book['title'].split()
            for word in title:
                if word.startswith(search_string):
                    matches_a_book_title = True
                    break
        if matches_first_name:
            search_results_fn.append(a)
        if matches_last_name:
            if a not in search_results_fn:
                search_results_ln.append(a)
        if matches_a_book_title:
            if a not in search_results_fn or a not in search_results_ln:
                search_results_bk.append(a)
    return search_results_fn+search_results_ln+search_results_bk


# ============================================
# Functions to convert model entities to dicts
# ============================================
def author_to_dict(author: Author):
    author_dict = {
        'full_name': author.full_name,
        'author_id': author.unique_id,
        'average_rating': author.ave_rating
    }
    return author_dict


def authors_to_dict(authors: Iterable[Author]):
    return [author_to_dict(au) for au in authors]


def book_to_dict(book: Book):
    book_dict = {
        'book_id': book.book_id,
        'release_year': book.release_year,
        'title': book.title,
        'authors': authors_to_dict(book.authors),
        'description': book.description
    }
    return book_dict


def books_to_dict(books: Iterable[Book]):
    return [book_to_dict(b) for b in books]

# ============================================
# Functions to convert dicts to model entities
# ============================================


def dict_to_author(a_dict):
    author = Author(a_dict.book_id, a_dict.full_name)
    # Note there's no comments or tags.
    return author
