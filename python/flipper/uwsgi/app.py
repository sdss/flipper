# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Filename: app.py
# Project: uwsgi
# Author: Brian Cherinka
# Created: Saturday, 7th September 2019 3:00:33 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2019 Brian Cherinka
# Last Modified: Saturday, 7th September 2019 3:01:11 pm
# Modified By: Brian Cherinka


from __future__ import print_function, division, absolute_import
from flipper.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

