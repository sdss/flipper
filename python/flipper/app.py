# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2018-05-15 10:51:48
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2018-08-16 11:19:45

from __future__ import print_function, division, absolute_import
import os
from flask import Flask
from flipper.controllers.index import index
from flipper.settings import ProdConfig, DevConfig, CustomConfig

# Set the Flipper version
__version__ = '0.1.4dev'


def create_app(debug=None, local=None, object_config=None):

    base = os.environ.get('FLIPPER_BASE', 'flipper')

    app = Flask(__name__, static_url_path='/{0}/static'.format(base))
    app.debug = debug

    url_prefix = '/flipper' if local else '/{0}'.format(base)

    # ----------------------------------
    # Load the appropriate Flask configuration object for debug or production
    if not object_config:
        if app.debug or local:
            app.logger.info('Loading Development Config!')
            object_config = type('Config', (DevConfig, CustomConfig), dict())
        else:
            app.logger.info('Loading Production Config!')
            object_config = type('Config', (ProdConfig, CustomConfig), dict())
    app.config.from_object(object_config)

    # -------------------
    # Registration
    register_blueprints(app, url_prefix=url_prefix)

    return app


def register_blueprints(app, url_prefix=None):
    ''' Register the Flask Blueprints used '''

    app.register_blueprint(index, url_prefix=url_prefix)


