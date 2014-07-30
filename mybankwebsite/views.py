__author__ = 'scottumsted'

from flask.templating import render_template
from flask import make_response, request, redirect
from mybankwebsite import app, cross_check, beginning_balance, balance, transactions


def csrf_check(handler):
    def decorator():
        token = request.args.get('cross_check', '')
        cookie = request.cookies.get('cross_check')
        result = None
        if cross_check.valid_token(token, cookie):
            result = handler()
        else:
            result = render_template('problem.html', problem='Request is not valid')
        return result
    return decorator


@app.route('/', methods=['GET'])
@app.route('/secure', methods=['GET'])
def display_secure():
    token, hashed = cross_check.generate_token()
    message = request.args.get('message', None)
    response = make_response(render_template('secure.html', token=token, message=message))
    response.set_cookie('cross_check', hashed)
    return response


@app.route('/unsecure', methods=['GET'])
def display_unsecure():
    message = request.args.get('message', None)
    response = make_response(render_template('unsecure.html',message=message))
    return response


@app.route('/withdrawal_secure', methods=['GET'])
@csrf_check
def withdrawal_secure():
    amount = request.args.get('amount')
    transactions.append(amount)
    balance['amount'] -= int(amount)
    return redirect('/secure?message=$'+amount+' withdrawn')


@app.route('/withdrawal_unsecure', methods=['GET'])
def withdrawal_unsecure():
    amount = request.args.get('amount')
    transactions.append(amount)
    balance['amount'] -= int(amount)
    return redirect('/unsecure?message=$'+amount+' withdrawn')


@app.route('/balance', methods=['GET'])
def display_balance():
    return render_template('balance.html', beginning_balance=beginning_balance['amount'], balance=balance['amount'], transactions=transactions)

