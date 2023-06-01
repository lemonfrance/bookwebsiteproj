from typing import List

from better_profanity import profanity
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

import library.adapters.repository as repo
import library.books.services as services
import library.utilities.utilities as utilities

reviews_blueprint = Blueprint(
    'reviews_bp', __name__
)


@reviews_blueprint.route('/write_review', methods=['GET', 'POST'])
@login_required
def write_review():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = ReviewForm()

    #If form successful
    if form.validate_on_submit():
        book_id = int(form.book_id.data)

        services.add_review(book_id, form.review_text.data, user_name, form.rating.data, repo.repo_instance)
        article = services.get_book(book_id, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('books_bp.display_book_info', view_reviews_for=book_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        book_id = int(request.args.get('book'))
        form.book_id.data = book_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        book_id = int(form.book_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    book = services.get_book(book_id, repo.repo_instance)
    return render_template(
        'book_reviews/user_write_review.html',
        title='Write Review',
        book=book,
        form=form,
        handler_url=url_for('reviews_bp.write_review')
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
    comment = TextAreaField('Review', [
        DataRequired(),
        Length(min=100, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    book_id = HiddenField("Book id")
    submit = SubmitField('Submit')
