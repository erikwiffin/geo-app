# pylint: disable=missing-docstring
""" Views module
"""
from itertools import groupby
from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from geo_app.extensions import arango

BP = Blueprint('main',
               __name__,
               template_folder='templates')


@BP.route('/')
def index():
    return render_template('main/index.jinja2')


@BP.route('/trip', methods=('POST',))
def start_trip():
    trip = {}
    res = arango.database('geo').collection('trips').insert(trip)

    start = request.form.get('start')
    if not start:
        start = arango.database('geo').aql.execute('''
        FOR dest IN destinations
            SORT RAND()
            LIMIT 1

            RETURN dest._key
        ''').next()

    parts = arango.database('geo').aql.execute('''
    FOR dest IN destinations
        FILTER dest._key == @start

        LET park = FIRST(
            FOR p IN NEAR(destinations, dest.lat, dest.lng)
                FILTER p.type == 'parks'
                LIMIT 1
                RETURN p
        )

        LET pilsner = FIRST(
            FOR p IN NEAR(destinations, dest.lat, dest.lng)
                FILTER p.type == 'pilsners'
                LIMIT 1
                RETURN p
        )

        LET pig = FIRST(
            FOR p IN NEAR(destinations, dest.lat, dest.lng)
                FILTER p.type == 'pigs'
                LIMIT 1
                RETURN p
        )

        RETURN {park, pilsner, pig}
    ''', bind_vars={'start': start}).next()

    if parts['park']:
        arango.database('geo').collection('parts').insert({
            '_from': res['_id'],
            '_to': parts['park']['_id'],
        })
    if parts['pilsner']:
        arango.database('geo').collection('parts').insert({
            '_from': res['_id'],
            '_to': parts['pilsner']['_id'],
        })
    if parts['pig']:
        arango.database('geo').collection('parts').insert({
            '_from': res['_id'],
            '_to': parts['pig']['_id'],
        })

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

    return render_template('main/trip.jinja2', trip=trip, parts=list(parts))


@BP.route('/search')
def search_parks():
    dests = arango.database('geo').aql.execute(
        '''
    FOR dest IN destinations
        SORT dest.name ASC

        LIMIT 500
        RETURN dest
        '''
    )

    keyfunc = lambda x: x.get('type')
    grouped = {}
    for k, v in groupby(sorted(dests, key=keyfunc), keyfunc):
        grouped[k] = list(v)

    return render_template('main/search.jinja2', **grouped)
