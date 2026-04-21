from __future__ import annotations

import copy
from pathlib import Path

import pytest

from flipper.Config import config


@pytest.fixture(autouse=True)
def restore_config_state():
    snapshot = {
        "base": config.base,
        "release": config.release,
        "available_releases": list(config.available_releases),
        "dev": config.dev,
        "skyserver_no_release": config.skyserver_no_release,
        "cfg": copy.deepcopy(config.cfg),
        "copyright_year": config.copyright_year,
        "mirror": config.mirror,
    }

    yield

    for key, value in snapshot.items():
        setattr(config, key, value)


@pytest.fixture
def sample_cfg():
    return {
        "base_url": "{{release}}.sdss.org",
        "wordpress_url": "www.sdss.org",
        "skyserver_release": 'dr19',
        "dev":{
            "wordpress_url": "https://testng.sdss.org",
            "skyserver_release": "/dr19",   
        },
        "title": "SDSS Splashpage",
        "sections": [
            {
                "rows": [
                    {
                        "cards": [
                            {
                                "title": "Internal",
                                "url": "/infrared/",
                            },
                            {
                                "title": "External",
                                "external_url": "https://example.com/{{release}}/docs",
                            },
                            {
                                "title": "Skyserver",
                                "use_skyserver": True,
                            },
                            {
                                "title": "WordPress",
                                "use_wordpress": True,
                                "url": "/news/",
                            },
                            {
                                "title": "Mirror",
                                "url": "/sas/",
                                "mirror": "mirror",
                                "picture": "logo.png",
                            },
                        ]
                    }
                ]
            }
        ],
    }


@pytest.fixture
def sample_template_dir(tmp_path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    (template_dir / "index.html").write_text(
        """<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="{{ url_for('static', filename='sdss-logo.png') }}">
  </head>
  <body>
    <h1>{{ title }}</h1>
    <p class="release">{{ release }}</p>
    {% for section in sections %}
      {% for row in section.rows %}
        {% for card in row.cards %}
          <a class="card" href="{{ card.href }}">{{ card.title }}</a>
        {% endfor %}
      {% endfor %}
    {% endfor %}
  </body>
</html>
""",
        encoding="utf-8",
    )
    return template_dir


@pytest.fixture
def sample_package_root(tmp_path):
    pkg_root = tmp_path / "flipper"
    template_dir = pkg_root / "templates"
    static_dir = pkg_root / "static"

    template_dir.mkdir(parents=True)
    static_dir.mkdir(parents=True)

    (template_dir / "index.html").write_text(
        """<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="{{ url_for('static', filename='sdss-logo.png') }}">
  </head>
  <body>
    <h1>{{ title }}</h1>
    <p class="release">{{ release }}</p>
    {% for section in sections %}
      {% for row in section.rows %}
        {% for card in row.cards %}
          <a class="card" href="{{ card.href }}">{{ card.title }}</a>
        {% endfor %}
      {% endfor %}
    {% endfor %}
  </body>
</html>
""",
        encoding="utf-8",
    )

    (static_dir / "sdss-logo.png").write_text("logo", encoding="utf-8")
    (static_dir / "site.css").write_text("body {}", encoding="utf-8")

    return pkg_root