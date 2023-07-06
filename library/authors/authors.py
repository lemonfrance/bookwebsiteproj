from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

import library.adapters.repository as repo
import library.authors.services as services
import library.utilities.utilities as utilities

authors_blueprint = Blueprint(
    'authors_bp', __name__
)


@authors_blueprint.route('/all_authors', methods=['GET'])
def all_authors():
    alphabetical_authors = services.get_sorted_authors(repo.repo_instance)

    for authors in alphabetical_authors:
        for author in alphabetical_authors[authors]:
            author['author_url'] = url_for('authors_bp.display_author_books', author_id=author['author_id'])

    # Generate the webpage to display all authors.
    return render_template(
        'authors/authors_all.html',
        title='Authors',
        all_categories=alphabetical_authors.keys(),
        all_authors=alphabetical_authors,
        lg_status=utilities.get_login_status(),
        username=utilities.get_username()
    )


@authors_blueprint.route('/display_author_books', methods=['GET'])
def display_author_books():
    # Read query parameters.
    author_id = request.args.get('author_id')

    author = ""
    books = []

    # Retrieve books from author id.
    try:
        author_id = int(author_id)
        # Retrieve author from author id.
        author = services.get_author(author_id, repo.repo_instance)
        # Retrieve books with author id.
        authored_books = services.get_author_books(author_id, repo.repo_instance)
        for ab in authored_books:
            ab['view_info_url'] = utilities.get_books_and_urls()[ab['book_id']]
            books += [ab]
    except services.NonExistentAuthorException:
        redirect(url_for('home_bp.home'))
    # Generate the webpage to display all books under the said author.
    return render_template(
        'authors/author_info.html',
        title=author['full_name'] + "'s Books",
        author=author,
        books=books,
        lg_status=utilities.get_login_status(),
        username=utilities.get_username()
    )
