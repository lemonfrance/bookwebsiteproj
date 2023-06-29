from flask import Blueprint, request, render_template, redirect, url_for, session

import library.adapters.repository as repo
import library.utilities.services as services

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_login_status():
    lg_status = False
    if "user_name" in session:
        lg_status = True
    # True = signed in, False = not signed in
    return lg_status


def get_username():
    username = ""
    if "user_name" in session:
        username = str(session['user_name'])
    return username


def get_five_latest_books():
    latest_books = services.get_year_sorted_books(repo.repo_instance)
    latest_books = latest_books[:5]
    for b in latest_books:
        b['view_info_url'] = get_books_and_urls()[b['book_id']]
    return latest_books


def get_top_five_books():
    top_five_books = services.get_ranked_books(repo.repo_instance)
    top_five_books = top_five_books[:5]
    for b in top_five_books:
        b['view_info_url'] = get_books_and_urls()[b['book_id']]
    return top_five_books


def get_top_five_authors():
    top_five_authors = services.get_ranked_authors(repo.repo_instance)
    top_five_authors = top_five_authors[:5]
    """
    for a in top_five_authors:
        a['view_info_url'] = get_authors_and_urls()[a['author_id']]
    """
    return top_five_authors


def get_authors_and_urls():
    authors = services.get_ranked_authors(repo.repo_instance)
    author_urls = dict()
    for a in authors:
        author_urls[a['author_id']] = url_for('authors_bp.all_authors', author=a['author_id'])
    return author_urls


def get_shelves_and_urls():
    shelf_names = services.get_shelf_names(repo.repo_instance)
    shelf_urls = dict()
    for s_name in shelf_names:
        shelf_urls[s_name] = url_for('books_bp.display_shelf_books', shelf_name=s_name)
    return shelf_urls


def get_books_and_urls():
    book_ids = services.get_book_ids(repo.repo_instance)
    book_urls = dict()
    for b_id in book_ids:
        book_urls[b_id] = url_for('books_bp.display_book_info', book_id=b_id,
                                  view_reviews_for=b_id)
    return book_urls


def get_selected_shelves(quantity):
    shelves = services.get_random_n_shelves(quantity, repo.repo_instance)
    for s in shelves:
        s['hyperlink'] = url_for('books_bp.display_by_shelves')
    return shelves


def get_last_five_sorted_rpreviews(username):
    user_reviews = services.get_user_reviews(username, repo.repo_instance)
    total_review_num = len(user_reviews)
    user_reviews = reversed(user_reviews[-5:])

    review_previews = list()

    for ur in user_reviews:
        b_id = ur['book'].book_id
        title = ur['book'].title
        rating = ur['rating']
        text = ur['review_text']

        if len(title) > 35:
            title = title[:32]+"..."
        if len(text) > 35:
            title = text[:32]+"..."

        review_previews += [
            ('"{}" ({}/5) - {}'.format(title, rating, text),
            url_for('books_bp.display_book_info', book_id=b_id,
                    view_reviews_for=b_id))
        ]

    # Returns the total number of reviews and a list containing tuples
    # of review preview data, particularly a preview text and a link to book_info.html.
    return [total_review_num, review_previews]
