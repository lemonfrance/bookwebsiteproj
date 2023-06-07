import abc
from typing import List

from library.domain.model import Book, Author, Review, User, Shelf, Publisher

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    # Book methods
    @abc.abstractmethod
    def add_book(self, book: Book):
        """" Adds a Book to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books(self) -> List[Book]:
        """" Returns the entire Book collection in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_id(self, book_id: int) -> Book:
        """ Returns the Book with the id 'id' from the repository.

        If there is no Book with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_publisher_by_book_id(self, book_id: int) -> Publisher:
        """ Returns the Book with the id 'id' from the repository.

                If there is no Book with the given id, this method returns None.
                """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_target_year(self, target_year: int) -> List[Book]:
        """ Returns a list of Books that were published on target_date.

        If there are no Books on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_books(self) -> int:
        """ Returns the number of unique Books in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_book(self) -> Book:
        """ Returns the first Book from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_book(self) -> Book:
        """ Returns the last Book from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_shelf_by_name(self, shelf_name) -> Shelf:
        """ Returns the Shelf named shelf_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_shelves(self) -> List[Shelf]:
        """ Returns a list of all existing shelves.
        If there are no shelves, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_author(self, author: Author) -> List[Book]:
        """ Returns a list of Books whose author names are similar to author_name.

        If there is no such Books, this method returns an empty list.
        """
        raise NotImplementedError

    # Author methods
    @abc.abstractmethod
    def get_all_authors(self) -> List[Author]:
        """" Adds an Author to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author):
        """" Adds an Author to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_author_by_id(self, author_id: int) -> Author:
        """ Returns the Author with the id 'id' from the repository.

        If there is no Author with the given id, this method returns None.
        """
        raise NotImplementedError

    # average rating ranking
    @abc.abstractmethod
    def get_books_by_ave_rating(self) -> List[Book]:
        """ Returns an ascending, sorted list of Books by their average ratings from the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors_by_ave_rating(self) -> List[Author]:
        """ Returns an ascending, sorted list of Authors by their average ratings from the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_shelves_by_ave_rating(self) -> List[Shelf]:
        """ Returns an ascending, sorted list of Shelves by their average ratings from the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_year(self) -> List[Book]:
        """ Returns an ascending, sorted list of Books by their release years from the repository."""
        raise NotImplementedError

    # Review methods
    @abc.abstractmethod
    def add_book_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with a Book and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.book is None or review not in review.book.reviews:
            raise RepositoryException('Review not correctly attached to a Book')

    @abc.abstractmethod
    def get_book_reviews(self, book: Book) -> List[Review]:
        """" Returns a list of Reviews of 'book' from the repository, otherwise it returns empty list. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_reviews(self, user: User) -> List[Review]:
        """" Returns a list of Reviews written by user from the repository. """
        raise NotImplementedError

    # User methods
    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User with the name user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_id(self, user_id) -> User:
        """ Returns the User with the ID user_id from the repository.

        If there is no User with the given user_id, this method returns None.
        """
        raise NotImplementedError
