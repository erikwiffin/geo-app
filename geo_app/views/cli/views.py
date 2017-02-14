''' CLI commands.
'''
import csv

from flask import Blueprint

from geo_app.application import app
from geo_app.extensions import arango


BP = Blueprint('cli', __name__)


@app.cli.command()
def initdb():
    ''' Initialize the database.
    '''
    try:
        db = arango.database('geo')
    except:
        db = arango.create_database('geo')

    db.collection('parts').truncate()
    db.collection('trips').truncate()

    coll = db.collection('destinations')
    coll.truncate()

    _import_collection(coll, 'parks')
    _import_collection(coll, 'pilsners')
    _import_collection(coll, 'peculiarities')


def _import_collection(coll, name):
    path = './data/{}.csv'.format(name)
    with open(path) as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if not row['lat'] or not row['lng']:
                continue
            document = {
                'lat': float(row['lat']),
                'lng': -1 * float(row['lng']),
                'name': row['name'].strip(),
                'type': name,
            }
            coll.insert(document)
