__author__ = 'scottumsted'

from flask.templating import render_template
from flask import make_response, request, redirect
from mybankwebsite import app, beginning_balance, balance, transactions
from mybankwebsite.csrf_check import CsrfCheck, csrf_check


@app.route('/', methods=['GET'])
@app.route('/secure', methods=['GET'])
def display_secure():
    cc = CsrfCheck()
    token, hashed = cc.generate_token()
    message = request.args.get('message', None)
    response = make_response(render_template('secure.html', token=token, message=message))
    response.set_cookie('csrf_check', hashed)
    return response


@app.route('/unsecure', methods=['GET'])
def display_unsecure():
    message = request.args.get('message', None)
    response = make_response(render_template('unsecure.html', message=message))
    return response


@app.route('/withdrawal_secure', methods=['GET'])
@csrf_check
def withdrawal_secure():
    amount = request.args.get('amount')
    transactions.append(amount)
    balance['amount'] -= int(amount)
    return redirect('/secure?message=$' + amount + ' withdrawn')


@app.route('/withdrawal_unsecure', methods=['GET'])
def withdrawal_unsecure():
    amount = request.args.get('amount')
    transactions.append(amount)
    balance['amount'] -= int(amount)
    return redirect('/unsecure?message=$' + amount + ' withdrawn')


@app.route('/balance', methods=['GET'])
def display_balance():
    return render_template('balance.html', beginning_balance=beginning_balance['amount'], balance=balance['amount'],
                           transactions=transactions)
