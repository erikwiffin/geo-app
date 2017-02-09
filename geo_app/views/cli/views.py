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
        db = arango.create_database('geo')
    except:
        db = arango.database('geo')

    try:
        coll = db.create_collection('park')
    except:
        coll = db.collection('park')
        coll.truncate()

    with open('./data/state-parks.csv') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            row['lat'] = float(row['lat'])
            row['lon'] = float(row['lon'])
            coll.insert(row)
