# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2018-05-15 10:51:48
# @Last modified by:   Brian
# @Last Modified time: 2018-06-05 16:36:58

from __future__ import print_function, division, absolute_import
from flask import Flask, render_template
import argparse

# --------------------------
# Parse command line options
# --------------------------
parser = argparse.ArgumentParser(description='Script to start Flask app.')
parser.add_argument('-d', '--debug', help='Launch app in debug mode.', action="store_true", required=False)
parser.add_argument('-p', '--port', help='Port to use in debug mode.', default=5000, type=int, required=False)

args = parser.parse_args()


app = Flask(__name__)


@app.route('/', endpoint='home')
@app.route('/index/', endpoint='index')
def index():
    output = {'title': 'SDSS Splashpage'}
    return render_template('index.html', **output)


if __name__ == '__main__':
    app.run(port=args.port, debug=args.debug)

