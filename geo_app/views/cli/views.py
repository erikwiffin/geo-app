''' CLI commands.
'''
import csv
import math

from bs4 import BeautifulSoup
from flask import Blueprint
import requests

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
    _import_collection(coll, 'pigs')


@app.cli.command()
def download_bbq():
    ''' Download the truecue list.
    '''
    html = requests.get('http://www.truecue.org/true-cue-nc/').text
    soup = BeautifulSoup(html, 'html.parser')

    list_items = soup.select('#page ul > li')

    with open('./data/pigs.raw.csv', 'w') as fh:
        fieldnames = ['name', 'lat', 'lng', 'url']
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        for item in list_items:
            link = item.select_one('a')
            if not link:
                print(item)
                continue
            row = {
                'name': link.get_text(),
                'lat': '',
                'lng': '',
                'url': link.get('href'),
            }
            writer.writerow(row)


@app.cli.command()
def download_beer():
    ''' Download the NC Beer Guys list.
    '''
    xml = requests.get('http://www.ncbeerguys.com/wp-content/uploads/wp-google-maps/1markers.xml?u=747').text
    soup = BeautifulSoup(xml, 'xml')

    markers = soup.select('marker')

    with open('./data/pilsners.raw.csv', 'w') as fh:
        fieldnames = ['name', 'lat', 'lng', 'url']
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for marker in markers:
            row = {
                'name': marker.title.get_text(),
                'lat': marker.lat.get_text(),
                'lng': marker.lng.get_text(),
                'url': marker.linkd.get_text(),
            }
            writer.writerow(row)


def _import_collection(coll, name):
    path = './data/{}.csv'.format(name)
    with open(path) as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if not row['lat'] or not row['lng']:
                continue
            document = {
                'lat': float(row['lat']),
                'lng': -1 * math.fabs(float(row['lng'])),
                'url': row.get('url'),
                'name': row['name'].strip(),
                'type': name,
            }
            coll.insert(document)
