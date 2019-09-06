# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2018-08-16 11:43:42
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2018-08-16 11:58:06

from __future__ import print_function, division, absolute_import
import pytest
from flask import url_for, request as freq
from flipper.app import create_app


@pytest.fixture
def app(monkeypatch, request):
    ''' Flask application '''
    app = create_app()
    return app


@pytest.yield_fixture
def testctx(monkeypatch):
    ''' Fixture to create an app with a test Flask base url

    Returns only the request context to allow for use for url_for

    '''
    monkeypatch.setenv('FLIPPER_BASE', 'test/flipper')
    app = create_app()
    app.testing = True
    ctx = app.test_request_context()
    ctx.push()
    yield
    ctx.pop()


def test_app(client):
    assert client.get(url_for('index.home')).status_code == 200


def test_ok_status(client):
    res = client.get(url_for('index.status'))
    assert res.json == {'flipper status': 'ok'}


def _get_urls(base):
    home = url_for('index.home')
    static = url_for('static', filename='sdss-logo.png')
    assert home == '{0}'.format(base)
    assert static == '{0}static/sdss-logo.png'.format(base)


def test_urls(client):
    ''' test of basic flipper urls '''
    _get_urls('/flipper/')


def test_testbase(testctx):
    ''' test of flipper test server urls '''
    _get_urls('/test/flipper/')
