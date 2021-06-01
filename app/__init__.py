#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""App init files"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
app.config["SECRET_KEY"]="secretkey"
db = SQLAlchemy(app)
Bootstrap(app)

from app import routes
from app.database import *

