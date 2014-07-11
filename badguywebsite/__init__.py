__author__ = 'scottumsted'
from flask import Flask
app = Flask(__name__)
app.config.from_envvar('BADGUY_SETTINGS', silent=False)
import badguywebsite.views

