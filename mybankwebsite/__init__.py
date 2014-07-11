__author__ = 'scottumsted'
from flask import Flask
app = Flask(__name__)
app.config.from_envvar('MYBANK_SETTINGS', silent=False)
beginning_balance = {'amount': 1000}
balance = {'amount': 1000}
transactions = []
import mybankwebsite.views


