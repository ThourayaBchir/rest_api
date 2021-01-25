from flask import Flask
from flask_restful import Api
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from flask_migrate import Migrate
# add logging

# migrate = Migrate()

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


app.config.from_object(Config)
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
ma = Marshmallow(app)

# to avoid cirular imports
from app.resources.accounts import AccountsList, Accounts    # noqa: E402
from app.resources.malls import MallsList, Malls    # noqa: E402
from app.resources.units import UnitsList, Units    # noqa: E402

api.add_resource(AccountsList, '/api/v1.0/accounts')
api.add_resource(Accounts, '/api/v1.0/accounts/<int:id>')

api.add_resource(MallsList, '/api/v1.0/malls', '/api/v1.0/accounts/<int:id>/malls')
api.add_resource(Malls, '/api/v1.0/malls/<int:id>',
                 '/api/v1.0/accounts/<int:id>/malls/<int:mall_id>')

api.add_resource(UnitsList, '/api/v1.0/units', '/api/v1.0/accounts/<int:id>/malls/<int:mall_id>/units')
api.add_resource(Units, '/api/v1.0/units/<int:id>',
                 '/api/v1.0/accounts/<int:id>/malls/<int:mall_id>/units/<int:unit_id>')
