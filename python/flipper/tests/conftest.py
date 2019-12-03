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
import os
from flask import url_for, template_rendered
from flipper.app import create_app
from contextlib import contextmanager


@contextmanager
def captured_templates(app):
    ''' Records which templates are used '''
    recorded = []

    def record(app, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record)
    yield recorded
    template_rendered.disconnect(record)


@pytest.fixture()
def get_templates(app):
    ''' Fixture that returns which jinja template used '''
    with captured_templates(app) as templates:
        yield templates


@pytest.fixture
def app():
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


@pytest.yield_fixture
def testclient(monkeypatch):
    ''' Fixture to create an app with a test Flask base url

    Returns the client fixture

    '''
    monkeypatch.setenv('FLIPPER_BASE', 'test/flipper')
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_app(client):
    res = client.get(url_for('index.home'))
    assert res.status_code == 200


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


# global releases to loop over
releases = ['dr15', 'dr16']


@pytest.fixture(params=releases)
def monkeyrelease(monkeypatch, request):
    ''' Fixture to monkeypatch the flipper release environment variable '''
    monkeypatch.setitem(os.environ, 'FLIPPER_RELEASE', request.param)
    yield request.param


def test_template(client, get_templates):
    ''' tests accessing a template and context '''
    res = client.get(url_for('index.home'))
    assert res.status_code == 200
    template, context = get_templates[0]
    assert template.name == 'index.html'
    assert context['title'] == 'SDSS Splashpage'


def test_base_release(monkeyrelease, client, get_templates):
    ''' test release changes using main base urls '''
    res = client.get(url_for('index.home'))
    template, context = get_templates[0]
    assert monkeyrelease == context['release']
    url = '{0}.sdss.org'.format(monkeyrelease)
    assert url in context['base_url']
    assert url in context['marvin_url']
    assert 'https://{0}/infrared/'.format(url) in str(res.data)


def test_test_release(monkeyrelease, testctx, testclient, get_templates):
    ''' tests release changes using the test base url '''
    res = testclient.get(url_for('index.home'))
    template, context = get_templates[0]
    assert monkeyrelease == context['release']
    url = '{0}.sdss.utah.edu'.format(monkeyrelease)
    assert url in context['base_url']
    assert 'lore.sdss.utah.edu/test' in context['marvin_url']
    assert 'https://{0}/infrared/'.format(url) in str(res.data)

