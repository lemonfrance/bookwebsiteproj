from typing import List

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

import library.adapters.repository as repo
import library.books.services as services
import library.utilities.utilities as utilities

books_blueprint = Blueprint(
    'books_bp', __name__
)


@books_blueprint.route('/display_all_books', methods=['GET'])
def display_all_books():
    books_per_page = 5

    # Read query parameters.
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)


    # Retrieve the batch of books to display on the Web page.
    all_books = services.get_all_books(repo.repo_instance)
    books = all_books[cursor:cursor + books_per_page]

    first_book_url = None
    last_book_url = None
    next_book_url = None
    prev_book_url = None

    if cursor > 0:
        # There are preceding books, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_book_url = url_for('books_bp.display_all_books', cursor = cursor - books_per_page)
        first_book_url = url_for('books_bp.display_all_books',)

    if cursor + books_per_page < len(all_books):
        # There are further books, so generate URLs for the 'next' and 'last' navigation buttons.
        next_book_url = url_for('books_bp.display_all_books', cursor=cursor + books_per_page)

        last_cursor = books_per_page * int(len(all_books) / books_per_page)
        if len(all_books) % books_per_page == 0:
            last_cursor -= books_per_page
        last_book_url = url_for('books_bp.display_all_books', cursor=last_cursor)

    # Construct urls for viewing book info.
    for b in books:
        b['view_info_url'] = utilities.get_books_and_urls()[b['book_id']]

    # Generate the webpage to display the articles.
    return render_template(
        'books/books_all.html',
        title='Our Book Collection',
        all_books=all_books,
        books=books,
        first_book_url=first_book_url,
        last_book_url=last_book_url,
        prev_book_url=prev_book_url,
        next_book_url=next_book_url,
        lg_status=utilities.get_login_status(),
        username=utilities.get_username()
    )


@books_blueprint.route('/display_by_shelves', methods=['GET'])
def display_by_shelves():
    books_per_page = 8

    # Read query parameters.
    shelf_name = request.args.get('shelf')

    all_shelves = services.get_all_shelves(repo.repo_instance)

    # Retrieve random shelf names to recommend
    random_20_shelf_names = utilities.get_selected_shelves(20)

    # If shelf_name is None, retrieve the batch of books per shelf in top 5 shelves to display on the Web page.
    # Else, retrieve batch of books based on shelf_name to display on the Web page.
    shelves_with_books = []
    all_view_urls = utilities.get_books_and_urls()
    if shelf_name is None:
        top_5_shelves = services.get_top_n_shelves(5,repo.repo_instance)
        for ts in top_5_shelves:
            book_ids = ts['shelved_books']
            shelf_books = [services.get_books_by_id(book_ids, repo.repo_instance)]
            for sb in shelf_books:
                sb['view_info_url'] = all_view_urls[sb['book_id']]
            shelves_with_books += [
                {
                    'name': [ts['name']],
                    'shelved_books': shelf_books
                }
            ]
    else:
        book_ids = services.get_shelf_data(shelf_name)['shelved_books']
        shelf_books = [services.get_books_by_id(book_ids, repo.repo_instance)]
        for sb in shelf_books:
            sb['view_info_url'] = all_view_urls[sb['book_id']]
        shelves_with_books += [
            {
                'name': shelf_name,
                'shelved_books': shelf_books
            }
        ]

    # Generate the webpage to display the shelves and books.
    return render_template(
        'books/books_all.html',
        title='Our Book Shelves',
        random_20_shelf_names=random_20_shelf_names,
        all_shelves=all_shelves,
        shelves=shelves_with_books,
        lg_status=utilities.get_login_status(),
        username=utilities.get_username()
    )


@books_blueprint.route('/display_book_info', methods=['GET'])
def display_book_info():
    # 1 book only

    # Read query parameters.
    book_id = request.args.get('book_id')
    book_to_show_reviews = request.args.get('view_reviews_for')

    if book_to_show_reviews is None:
        book_to_show_reviews = -1
    else:
        book_to_show_reviews = int(book_to_show_reviews)

    # Retrieve book from book_id.
    try:
        book = services.get_book(int(book_id), repo.repo_instance)
    except services.NonExistentBookException:
        redirect(url_for('home_bp.home'))

    # Construct urls for viewing book reviews and writing reviews.
    book['view_review_url'] = url_for('books_bp.display_book_info', book=book['book_id'],
                                      view_reviews_for=book['book_id'])
    # if logged in: go to write review page. otherwise: go to login page
    # book['write_review_url'] = url_for('auth_bp.login', book=book['book_id'])
    #book['write_review_url'] = url_for('reviews_bp.write_book_review', book=book['book_id'])

    # Generate the webpage to display the articles.
    return render_template(
        'books/book_info.html',
        title=book['title'],
        book=book,
        shelf_urls=utilities.get_shelves_and_urls(),
        show_reviews_for_book=book_to_show_reviews,
        lg_status=utilities.get_login_status(),
        username=utilities.get_username()
    )
