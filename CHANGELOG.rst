.. _flipper-changelog:

Flipper Change Log
==================
0.1.4 (2025-05-29)
------------------
- Add Zora and update for DR19/SDSS-V
- Removed SDSS Blog
- Add SDSS Bluesky link
- Add save static site option with run_flipper
- Add flag for using testng developement links with run_flipper
- Add option to manually set release with run_flipper

0.1.3 (2021-11-04)
------------------
- Added support for webp image format.  Updated all images to webp for better performance.
- Added DR17 release

0.1.2 (2018-12-03)
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
- now also uses proxy set request header for nginx locations that are proxies
- now assumes testing urls will be lore.sdss.utah.edu (or sas.sdss.org/test) and production urls are [release].sdss.org
- flipper now looks for release from request header variable first, then FLIPPER_RELEASE environment variable

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


