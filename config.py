import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ENV = os.getenv('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'rest_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
