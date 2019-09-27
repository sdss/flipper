.. _flipper-changelog:

Flipper Change Log
==================

0.1.2 (unreleased)
------------------

Added
^^^^^
- added test server for flipper with new uwsgi test.ini
- added new FLIPPER_BASE envvar to allow for test server 
- added flipper version to page footer 
- added new FLIPPER_RELEASE environment variable which controls for DR versioning

Changed
^^^^^^^
- Updating links for DR16
- Set up flipper to be more flexible towards releases
- Flipper index page now accepts a base_url to control for production, testing environments and for changing releases
- now uses uwsgi_param on nginx locations to determine flipper release, DR15, DR16, etc.
- now assumes testing urls will be [release].sdss.utah.edu and production urls are [release].sdss.org

0.1.1 (2018-11-30)
------------------

Changed
^^^^^^^
* Splash page to hires version
* Switched Data Interaction links to dr15
* Added new SDSS Blog to EPO
* Added new images to each thumbnail and new text. 
* switched css border to small divider

.. _changelog-0.1.0:

0.1.0 (2018-08-16)
------------------

This is the first version of the SDSS flipper app.

Added
^^^^^
* Initial creation.
* Added uwsgi production.ini and local.ini files
* Added bin/run_flipper script for production run
* Added .bumpversion.cfg
* Flask settings.py
* Added some basic tests
* Adding a pipenv PipFile for prod+dev dependencies


