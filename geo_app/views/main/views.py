# pylint: disable=missing-docstring
""" Views module
"""
from flask import (
    Blueprint,
    render_template,
)

from geo_app.extensions import arango

BP = Blueprint('main',
               __name__,
               template_folder='templates')


@BP.route('/')
def index():
    parks = arango.database('geo').aql.execute('''
    FOR p1 IN park
        SORT RAND()
        LIMIT 1

        FOR p2 IN NEAR(park, p1.lat, p1.lon, 2)
            FILTER p2 != p1
            RETURN {p1, p2}
    ''').next()

    return render_template('index.jinja2', **parks)
