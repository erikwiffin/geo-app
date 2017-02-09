# pylint: disable=missing-docstring
import json

import jinja2

from geo_app.application import app


@app.template_filter('jsonify')
def jsonify_filter(target):
    return json.dumps(target)
