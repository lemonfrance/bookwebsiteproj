from flask import Blueprint, render_template

import library.utilities.utilities as utilities


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        title="Home",
        five_latest_books=utilities.get_five_latest_books(),
        five_top_books=utilities.get_top_five_books(),
        five_top_authors=utilities.get_top_five_authors()
    )
