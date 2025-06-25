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
from flipper.controllers.index import index, set_wordpress_url, set_release
from flipper.settings import ProdConfig, DevConfig, CustomConfig

# Set the Flipper version
__version__ = '0.1.4dev'


def create_app(debug=None, local=None, object_config=None, dev=False, release=None, 
               skyserver_no_release=False):

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
    register_blueprints(app, url_prefix=url_prefix, dev=dev, release=release, 
                        skyserver_no_release=skyserver_no_release)

    return app


def register_blueprints(app, url_prefix=None, dev=False, release=None, skyserver_no_release=False):
    ''' Register the Flask Blueprints used '''

    set_wordpress_url(dev=dev)
    set_release(release=release, skyserver_no_release=skyserver_no_release)

    app.register_blueprint(index, url_prefix=url_prefix)


def save_rendered_page(app, route='/flipper/', output_dir='deploy'):
    import shutil
    import os

    with app.test_request_context(route):
        response = app.full_dispatch_request()
        html = response.get_data(as_text=True)

        html = html.replace('/flipper/static/', './flipper/static/')

        # Fix absolute paths to relative ones

        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Saved HTML to {os.path.join(output_dir, 'index.html')}")

        static_src = os.path.join(app.root_path, 'static')
        static_dst = os.path.join(output_dir,'flipper','static')
        if os.path.exists(static_src):
            shutil.copytree(static_src, static_dst, dirs_exist_ok=True)
            print(f"Copied static files to {static_dst}")
        else:
            print("No static directory found to copy.")

