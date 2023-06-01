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
    authors_per_page = 5

    # Read query parameters.
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    # Retrieve all authors and the batch of books to display on the Web page.
    all_authors = services.get_all_authors(repo.repo_instance)
    authors = all_authors[cursor:cursor + authors_per_page]

    first_au_url = None
    last_au_url = None
    next_au_url = None
    prev_au_url = None

    if cursor > 0:
        # There are preceding books, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_au_url = url_for('books_bp.display_all_books', cursor=cursor - authors_per_page)
        first_au_url = url_for('books_bp.display_all_books', )

    if cursor + authors_per_page < len(authors):
        # There are further books, so generate URLs for the 'next' and 'last' navigation buttons.
        next_au_url = url_for('books_bp.display_all_books', cursor=cursor + authors_per_page)

        last_cursor = authors_per_page * int(len(authors) / authors_per_page)
        if len(authors) % authors_per_page == 0:
            last_cursor -= authors_per_page
        last_au_url = url_for('books_bp.display_by_shelves', cursor=last_cursor)

    # Construct urls for viewing book info.
    for b in authors:
        b['view_info_url'] = utilities.get_authors_and_urls()[b['author_id']]

    # Generate the webpage to display the articles.
    return render_template(
        'authors/authors_all.html',
        title='Our Author Collection',
        all_authors=all_authors,
        authors=authors,
        first_au_url=first_au_url,
        last_au_url=last_au_url,
        prev_au_url=prev_au_url,
        next_au_url=next_au_url
    )
