# pylint: disable=missing-docstring
""" Views module
"""
from flask import (
    Blueprint,
    redirect,
    render_template,
    url_for,
)

from geo_app.extensions import arango

BP = Blueprint('main',
               __name__,
               template_folder='templates')


@BP.route('/')
def index():
    return render_template('index.jinja2')


@BP.route('/trip', methods=('POST',))
def start_trip():
    trip = {}
    res = arango.database('geo').collection('trips').insert(trip)

    parts = arango.database('geo').aql.execute('''
    FOR dest IN destinations
        SORT RAND()
        LIMIT 1

        LET park = FIRST(
            FOR p IN NEAR(destinations, dest.lat, dest.lng)
                FILTER p.type == 'parks'
                LIMIT 1
                RETURN p
        )

        LET peculiarity = FIRST(
            FOR p IN NEAR(destinations, dest.lat, dest.lng)
                FILTER p.type == 'peculiarities'
                LIMIT 1
                RETURN p
        )

        RETURN {park, peculiarity}
    ''').next()

    arango.database('geo').collection('parts').import_bulk([
        {
            '_from': res['_id'],
            '_to': parts['park']['_id'],
        },
        {
            '_from': res['_id'],
            '_to': parts['peculiarity']['_id'],
        },
    ])

    return redirect(url_for('.trip', trip_id=res['_key']))


@BP.route('/trip/<trip_id>')
def trip(trip_id):
    trip = arango.database('geo').collection('trips').get(trip_id)

    parts = arango.database('geo').aql.execute('''
    FOR t IN trips
        FILTER t._key == @key
        FOR c IN OUTBOUND t GRAPH 'parts'
            return c
   ''', bind_vars={'key': trip_id})

    return render_template('trip.jinja2', trip=trip, parts=list(parts))
