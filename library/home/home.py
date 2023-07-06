from flask import Blueprint, render_template, url_for

import library.utilities.utilities as utilities

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    top_five_authors = utilities.get_top_five_authors()

    for author in top_five_authors:
        author['author_url'] = url_for('authors_bp.display_author_books', author_id=author['author_id'])

    return render_template(
        'home/home.html',
        title="Home",
        five_latest_books=utilities.get_five_latest_books(),
        five_top_books=utilities.get_top_five_books(),
        five_top_authors=top_five_authors,
        lg_status=utilities.get_login_status(),
        username=utilities.get_username()
    )


@home_blueprint.route('/account', methods=['GET'])
def account():
    username = utilities.get_username()
    last_five_rpreviews = utilities.get_last_five_sorted_rpreviews(username)
    return render_template(
        'home/account.html',
        title="Welcome, " + username + "!",
        lg_status=utilities.get_login_status(),
        username=utilities.get_username(),
        reviews_num=last_five_rpreviews[0],
        review_previews=last_five_rpreviews[1]
    )
