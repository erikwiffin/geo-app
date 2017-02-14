# pylint: disable=missing-docstring
import os

from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app.config['ARANGODB_DATABASE_URI'] = os.getenv('ARANGODB_DATABASE_URI')
app.config['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')


def create_app():
    from geo_app import (
        extensions,
        filters,
    )
    from geo_app.views.cli.views import BP as cli_blueprint
    from geo_app.views.main.views import BP as main_blueprint

    app.register_blueprint(cli_blueprint)
    app.register_blueprint(main_blueprint)

    extensions.arango.init_app(app)

    return app
