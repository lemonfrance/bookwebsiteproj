import json
from typing import List

from library.domain.model import Publisher, Author, Book, User, Review, Shelf, make_shelf_association


class GeneralJSONReader:
    def __init__(self, users_file_name: str, books_file_name: str, authors_file_name: str, reviews_file_name: str):
        self.__users_file_name = users_file_name
        self.__books_file_name = books_file_name
        self.__authors_file_name = authors_file_name
        self.__reviews_file_name = reviews_file_name

    def read_users_file(self) -> list:
        users_json = []
        with open(self.__users_file_name, encoding='UTF-8') as users_jsonfile:
            for line in users_jsonfile:
                user_entry = json.loads(line)
                users_json.append(user_entry)
        return users_json

    def read_books_file(self) -> list:
        books_json = []
        with open(self.__books_file_name, encoding='UTF-8') as books_jsonfile:
            for line in books_jsonfile:
                book_entry = json.loads(line)
                books_json.append(book_entry)
        return books_json

    def read_authors_file(self) -> list:
        authors_json = []
        with open(self.__authors_file_name, encoding='UTF-8') as authors_jsonfile:
            for line in authors_jsonfile:
                author_entry = json.loads(line)
                authors_json.append(author_entry)
        return authors_json

    def read_reviews_file(self) -> list:
        reviews_json = []
        with open(self.__reviews_file_name, encoding='UTF-8') as reviews_jsonfile:
            for line in reviews_jsonfile:
                review_entry = json.loads(line)
                reviews_json.append(review_entry)
        return reviews_json


class BooksJSONReader(GeneralJSONReader):
    def __init__(self, users_file_name: str, books_file_name: str, authors_file_name: str, reviews_file_name: str):
        super().__init__(users_file_name, books_file_name, authors_file_name, reviews_file_name)
        self.__dataset_of_books: List[Book] = []

    @property
    def dataset_of_books(self) -> List[Book]:
        return self.__dataset_of_books

    def read_json_files(self):
        books_json = self.read_books_file()
        authors_json = self.read_authors_file()

        for book_json in books_json:
            book_instance = Book(int(book_json['book_id']), book_json['title'], book_json['url'],
                                 book_json['image_url'])
            book_instance.publisher = Publisher(book_json['publisher'])
            if book_json['publication_year'] != "":
                book_instance.release_year = int(book_json['publication_year'])
            if book_json['is_ebook'].lower() == 'false':
                book_instance.ebook = False
            else:
                if book_json['is_ebook'].lower() == 'true':
                    book_instance.ebook = True
            book_instance.description = book_json['description']
            if book_json['num_pages'] != "":
                book_instance.num_pages = int(int(book_json['num_pages']))

            book_instance.ave_rating = float(book_json['average_rating'])
            book_instance.publisher = Publisher(book_json['publisher'])
            for ps in book_json['popular_shelves']:
                # connect shelf to book
                new_shelf = Shelf(ps['name'])
                make_shelf_association(book_instance, new_shelf)

            # extract the author ids:
            list_of_authors_ids = book_json['authors']
            for author_id in list_of_authors_ids:

                numerical_id = int(author_id['author_id'])
                # We assume book authors are available in the authors file,
                # otherwise more complex handling is required.
                author_name = None
                for author_json in authors_json:
                    if int(author_json['author_id']) == numerical_id:
                        author_name = author_json['name']
                book_instance.add_author(Author(numerical_id, author_name))

            self.__dataset_of_books.append(book_instance)


class AuthorsJSONReader(GeneralJSONReader):
    def __init__(self, users_file_name: str, books_file_name: str, authors_file_name: str, reviews_file_name: str):
        super().__init__(users_file_name, books_file_name, authors_file_name, reviews_file_name)
        self.__dataset_of_authors: List[Author] = []

    @property
    def dataset_of_authors(self) -> List[Author]:
        return self.__dataset_of_authors

    def read_json_files(self):
        authors_json = self.read_authors_file()
        books_json = self.read_books_file()
        for aj in authors_json:
            current_author_id = int(aj['author_id'])
            author_instance = Author(current_author_id, aj['name'])
            author_instance.ave_rating = float(aj['average_rating'])
            # get coauthors from books file, extract the author ids
            for bj in books_json:
                list_of_authors_ids = bj['authors']  # [{},{}]
                authors = []  # contains author ids
                for author_id in list_of_authors_ids:
                    authors += [int(author_id['author_id'])]
                if current_author_id in authors:
                    for a_id in authors:
                        if a_id != current_author_id:
                            author_instance.add_coauthor(a_id)
            self.__dataset_of_authors.append(author_instance)


class ReviewsJSONReader(GeneralJSONReader):
    def __init__(self, users_file_name: str, books_file_name: str, authors_file_name: str, reviews_file_name: str):
        super().__init__(users_file_name, books_file_name, authors_file_name, reviews_file_name)
        self.__dataset_of_reviews: List[Review] = []

    @property
    def dataset_of_reviews(self) -> List[Review]:
        return self.__dataset_of_reviews

    def read_json_files(self):
        reviews_json = self.read_reviews_file()
        books_json = self.read_books_file()
        authors_json = self.read_authors_file()

        if reviews_json:
            for rj in reviews_json:
                rj_book = None
                for bj in books_json:
                    if int(bj['book_id']) == int(rj['book_id']):
                        rj_book = Book(int(bj['book_id']), bj['title'], bj['url'], bj['image_url'])
                        rj_book.release_year = int(bj['publication_year'])
                        rj_book.ave_rating = float(bj['average_rating'])
                        for author in bj['authors']:
                            a_id = int(author['author_id'])
                            full_name = ""
                            for aj in authors_json:
                                if a_id == int(aj['author_id']):
                                    full_name = aj['name']
                                    break
                            a = Author(a_id, full_name)
                            rj_book.add_author(a)
                        break
                user_inst = User(rj['user']['user_name'], rj['user']['password'])
                review_instance = Review(user_inst, rj_book, rj['review_text'], int(rj['rating']))
                self.__dataset_of_reviews.append(review_instance)


class UsersJSONReader(GeneralJSONReader):
    def __init__(self, users_file_name: str, books_file_name: str, authors_file_name: str, reviews_file_name: str):
        super().__init__(users_file_name, books_file_name, authors_file_name, reviews_file_name)
        self.__dataset_of_users: List[User] = []

    @property
    def dataset_of_users(self) -> List[User]:
        return self.__dataset_of_users

    def read_json_files(self):
        users_json = self.read_users_file()
        reviews_json = self.read_reviews_file()
        books_json = self.read_books_file()

        if users_json:
            for uj in users_json:
                un = uj['user_name']
                pw = uj['password']
                user_instance = User(un, pw)
                for book_id in uj['read_books']:
                    for bj in books_json:
                        if int(bj['book_id']) == int(book_id):
                            book = Book(int(book_id), bj['title'], bj['url'], bj['image_url'])
                            user_instance.read_a_book(book)
                            break
                for rj in reviews_json:
                    if rj['user']['user_name'] == un:
                        for bj in books_json:
                            if int(bj['book_id']) == int(rj['book_id']):
                                book = Book(int(bj['book_id']), bj['title'], bj['url'], bj['image_url'])
                                r = Review(un, book, rj['review_text'], int(rj['rating']))
                                user_instance.add_review(r)
                                break
                self.__dataset_of_users.append(user_instance)
