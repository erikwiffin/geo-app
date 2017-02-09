from arango import ArangoClient
from furl import furl


class ArangoExtension(ArangoClient):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        url = furl(app.config['ARANGODB_DATABASE_URI'])

        super().__init__(
            protocol=url.scheme,
            host=url.host,
            port=url.port,
            username=url.username,
            password=url.password,
            enable_logging=True,
        )
