#!/usr/bin/env python
import sys
from flask import Flask, request
from functools import wraps

app = Flask(__name__)

is_teapot = sys.argv[-1] == '--teapot'
available_additions = ['milk', 'chocolate']

app.brewing = None


def method(fx):
    @wraps(fx)
    def wr():
        if is_teapot:
            return '', 418
        res = fx()
        extra_headers = {
            'Additions-List': ';'.join(available_additions)
        }
        if len(res) > 2:
            res[-1].update(extra_headers)
        else:
            res = res + (extra_headers,)
        return res
    return wr
        

@app.route('/', methods=['BREW'])
@method
def brew():
    rq_additions = request.headers.get('Accept-Additions', '')
    rq_additions = rq_additions.split(';')
    for addition in rq_additions:
        if addition and not addition in available_additions:
            return 'Invalid additions', 406
    app.brewing = rq_additions
    return 'OK', 200


@app.route('/', methods=['GET'])
@method
def get():
    if not app.brewing:
        return 'No coffee', 404
    res = 'Complete: coffee with %s' % ', '.join(app.brewing)
    app.brewing = None
    return res, 200


@app.route('/', methods=['PROPFIND'])
@method
def metadata():
    return '', 200


if __name__ == "__main__":
    app.run()