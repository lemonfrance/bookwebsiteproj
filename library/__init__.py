from flask import Flask, render_template
from pathlib import Path
import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository, populate

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('library') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill the content of the repository from the provided csv files
    populate(data_path, repo.repo_instance)

    # Build the application - these steps require an application context.
    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .books import books_blueprint
        app.register_blueprint(books_blueprint.books_blueprint)

        from .authors import authors
        app.register_blueprint(authors.authors_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        # TODO: register more blueprints

    return app
