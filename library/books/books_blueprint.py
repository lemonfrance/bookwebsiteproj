from typing import List

import wtforms.fields
from better_profanity import profanity
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, TextAreaField, HiddenField, IntegerRangeField, StringField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange, InputRequired

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
        prev_book_url = url_for('books_bp.display_all_books', cursor=cursor - books_per_page)
        first_book_url = url_for('books_bp.display_all_books', )

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
    alphabetical_shelves = services.categorize_shelves(repo.repo_instance)

    for shelves in alphabetical_shelves:
        for shelf in alphabetical_shelves[shelves]:
            shelf['shelf_url'] = url_for('books_bp.display_shelf_books', shelf_name=shelf['name'])

    # Generate the webpage to display the shelves and books.
    return render_template(
        'books/books_by_shelves.html',
        title='Our Book Shelves',
        all_categories=alphabetical_shelves.keys(),
        all_shelves=alphabetical_shelves,
        lg_status=utilities.get_login_status(),
        username=utilities.get_username()
    )


@books_blueprint.route('/display_shelf_books', methods=['GET'])
def display_shelf_books():
    # Read query parameters.
    shelf_name = request.args.get('shelf_name')

    # Retrieve shelf from shelf_name.
    try:
        shelf = services.get_shelf_data(shelf_name, repo.repo_instance)
        shelved_books = shelf['shelved_books']
        books = []
        for sb in shelved_books:
            b = services.get_book(sb, repo.repo_instance)
            b['view_info_url'] = utilities.get_books_and_urls()[b['book_id']]
            books += [b]
        # Generate the webpage to display all books under the shelf.
        return render_template(
            'books/shelf_list_books.html',
            title='Shelf',
            shelf=shelf,
            books=books,
            lg_status=utilities.get_login_status(),
            username=utilities.get_username()
        )
    except services.NonExistentShelfException:
        redirect(url_for('home_bp.home'))


@books_blueprint.route('/display_book_info', methods=['GET'])
def display_book_info():
    # 1 book only

    # Read query parameters.
    book_id = request.args.get('book_id')
    # Retrieve book from book_id.
    try:
        book = services.get_book(int(book_id), repo.repo_instance)
        # Construct urls for viewing book reviews and writing reviews.
        # if logged in: go to write review page. otherwise: go to login page
        if 'user_name' in session:
            book['write_review_url'] = url_for('books_bp.write_review', book_id=book['book_id'])
        else:
            book['write_review_url'] = url_for('authentication_bp.login')

        for author in book['authors']:
            author['author_url'] = url_for('authors_bp.display_author_books', author_id=author['author_id'])

        # Generate the webpage to display book info.
        return render_template(
            'books/book_info.html',
            title=book['title'],
            book=book,
            shelf_urls=utilities.get_shelves_and_urls(),
            lg_status=utilities.get_login_status(),
            username=utilities.get_username()
        )

    except services.NonExistentBookException:
        redirect(url_for('home_bp.home'))


@books_blueprint.route('/write_review', methods=['GET', 'POST'])
def write_review():
    user_name = session['user_name']
    form = ReviewForm()

    # If form successful
    if form.validate_on_submit():
        book_id = int(form.book.data)
        services.add_review(book_id, user_name, form.review.data, form.rating.data, repo.repo_instance)
        book = services.get_book(book_id, repo.repo_instance)
        return redirect(url_for('books_bp.display_book_info', book_id=book['book_id']))

    if request.method == 'GET':
        book_id = int(request.args.get('book_id'))
        form.book.data = book_id
    else:
        book_id = int(form.book.data)
    book = services.get_book(book_id, repo.repo_instance)
    return render_template(
        'book_reviews/write_review.html',
        title='Write Review',
        book=book,
        form=form,
        handler_url=url_for('books_bp.write_review', book_id=book['book_id']),
        lg_status=utilities.get_login_status(),
        username=utilities.get_username()
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review:', [
        DataRequired(message='Review must not be empty.'),
        Length(max=256, message='Review length is past the maximum length.'),
        ProfanityFree(message='Your review must not contain profanity.')])
    rating = SelectField(label='Rating:', validators=[
        InputRequired(),
        NumberRange(min=0, max=5, message="You can only rate from 0 to 5.")],
        coerce=int, choices=[0, 1, 2, 3, 4, 5])
    book = HiddenField("Book id")
    submit = SubmitField('Submit')
