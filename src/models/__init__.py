import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

CUR_DIR = os.path.abspath(os.curdir)
MODULE_DIR = os.path.join(CUR_DIR, "models")

__all__ = [f.replace('.py', '') for f in os.listdir(MODULE_DIR) if
           os.path.isfile(os.path.join(MODULE_DIR, f)) and not f.startswith('__')]

import src.app as app

engine = create_engine(app.app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app.app)
