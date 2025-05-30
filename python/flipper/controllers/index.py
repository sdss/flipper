# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2018-08-15 16:39:51
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2018-08-16 11:58:34

from __future__ import print_function, division, absolute_import
import os
import flipper.app
from flask import Blueprint, render_template, jsonify, request

index = Blueprint("index", __name__)

# SDSS DR releases
releases = ['dr15', 'dr16', 'dr17', 'dr18', 'dr19']
#wordpress_url = 'testng.sdss.org' 
wordpress_url = 'www.sdss.org'
skyserver_release = None

def set_wordpress_url(dev=False):
    # set testng url for testing links before rollout of release
    global wordpress_url, skyserver_release
    if dev:
        wordpress_url = 'testng.sdss.org' 
        skyserver_release = ''


def set_release(release = None):
    # Manaully set the release for this app instance deploy
    global releases 
    if release is not None:
        releases = [release]

custom_option = None  # This will be set by main app





@index.route('/status/', methods=['GET', 'POST'], endpoint='status')
def status():
    return jsonify({'flipper status': 'ok'})


@index.route('/', methods=['GET'], endpoint='home')
@index.route('/index/', methods=['GET'], endpoint='index')
def home():
    # get release from request header
    release = request.headers.get('Release', None)

    # if no release, get release variable from Flask request
    if not release:
        release = request.environ.get('FLIPPER_RELEASE', None)

    # if no release try the os environment variable
    if not release:
        release = os.environ.get("FLIPPER_RELEASE", None)

    # if no release, select the lastest one
    if not release:
        sorted_rels = sorted(releases, key=lambda x: int(x.split('dr')[-1]))
        release = sorted_rels[-1]

    # set base and marvin urls for production or testing
    istestenv = 'test' in request.path
    if istestenv:
        base_url = 'sas.sdss.org/test'
        marvin_url = 'lore.sdss.utah.edu/test'
    else:
        base_url = '{0}.sdss.org'.format(release)
        marvin_url = base_url

    global skyserver_release
    if skyserver_release is None:
        skyserver_release = '/{0}'.format(release)

    # build template parameter dictionary
    output = {'title': 'SDSS Splashpage', 'version': flipper.app.__version__,
              'release': release, 'istest': istestenv, 'base_url': base_url,
              'marvin_url': marvin_url, 'wordpress_url': wordpress_url, 
              'skyserver_release': skyserver_release}
    return render_template('index.html', **output)
