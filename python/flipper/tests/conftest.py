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
from flask import template_rendered
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


@pytest.fixture
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


@pytest.fixture
def testclient(monkeypatch):
    ''' Fixture to create an app with a test Flask base url

    Returns the client fixture

    '''
    monkeypatch.setenv('FLIPPER_BASE', 'test/flipper')
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


# global releases to loop over
releases = ['dr15', 'dr16']


@pytest.fixture(params=releases)
def monkeyrelease(monkeypatch, request):
    ''' Fixture to monkeypatch the flipper release environment variable '''
    monkeypatch.setitem(os.environ, 'FLIPPER_RELEASE', request.param)
    yield request.param

@pytest.fixture
def client(app):
    return app.test_client()