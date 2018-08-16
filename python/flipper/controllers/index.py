# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2018-08-15 16:39:51
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2018-08-15 17:05:32

from __future__ import print_function, division, absolute_import
from flask import Blueprint, render_template, jsonify

index = Blueprint("index", __name__)


@index.route('/status/', methods=['GET', 'POST'], endpoint='status')
def status():
    return jsonify(result={'flipper status': 'ok'})


@index.route('/', methods=['GET'], endpoint='home')
@index.route('/index/', methods=['GET'], endpoint='index')
def home():
    output = {'title': 'SDSS Splashpage'}
    return render_template('index.html', **output)
