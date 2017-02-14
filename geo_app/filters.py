# pylint: disable=missing-docstring
from datetime import datetime
import json

import jinja2

from geo_app.application import app


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.template_filter('jsonify')
def jsonify_filter(target):
    return json.dumps(target)
