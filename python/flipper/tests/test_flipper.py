from __future__ import annotations

import copy
from contextlib import contextmanager

from flipper.Config import config
from flipper.build import build_context, build_flipper, create_env, render_index, save_rendered_page
from flipper.index import load_sections_from_yaml, resolve_release


def test_resolve_release_prefers_explicit():
    config.available_releases = ["dr19", "dr20"]
    assert resolve_release("dr19", None) == "dr19"


def test_resolve_release_defaults_to_latest():
    config.available_releases =  ["dr19", "dr20"]
    assert resolve_release(None, None) == "dr20"


def test_build_context_replaces_release_in_base_url():
    config.release = "dr19"
    config.cfg = {
        "base_url": "{{release}}.sdss.org",
        "wordpress_url": "www.sdss.org",
        "skyserver_release": "/dr19",
    }

    ctx = build_context()

    assert ctx["release"] == "dr19"
    assert ctx["base_url"] == "dr19.sdss.org"
    assert ctx["wordpress_url"] == "www.sdss.org"
    assert ctx["skyserver_release"] == "/dr19"


def test_load_sections_from_yaml_builds_hrefs(sample_cfg):
    config.release = "dr19"
    config.mirror = "mirror"
    config.cfg = copy.deepcopy(sample_cfg)

    sections = load_sections_from_yaml()
    cards = sections[0]["rows"][0]["cards"]

    assert cards[0]["href"] == "https://dr19.sdss.org/infrared/"
    assert cards[1]["href"] == "https://example.com/dr19/docs"
    assert cards[2]["href"] == "https://skyserver.sdss.org/dr19"
    assert cards[3]["href"] == "https://www.sdss.org/news/"
    assert cards[4]["href"] == "https://mirror.sdss.org/sas/"
    assert cards[4]["picture"] == "mirror"


def test_render_index_renders_template_and_url_for(sample_template_dir):
    env = create_env(template_dir=str(sample_template_dir))

    context = {
        "title": "SDSS Splashpage",
        "version": "test",
        "release": "dr19",
        "base_url": "dr19.sdss.org",
        "wordpress_url": "www.sdss.org",
        "skyserver_release": "/dr19",
        "copyright_year": 2026,
    }
    sections = [
        {
            "rows": [
                {
                    "cards": [
                        {
                            "title": "Internal",
                            "href": "https://dr19.sdss.org/infrared/",
                        }
                    ]
                }
            ]
        }
    ]

    html = render_index(env, context, sections)

    assert "SDSS Splashpage" in html
    assert "dr19" in html
    assert "/static/sdss-logo.png" in html
    assert "https://dr19.sdss.org/infrared/" in html


def test_save_rendered_page_writes_files(tmp_path):
    static_src = tmp_path / "static"
    static_src.mkdir()
    (static_src / "sdss-logo.png").write_text("logo", encoding="utf-8")

    output_dir = tmp_path / "deploy"
    html = '<html><body><link href="/static/sdss-logo.png"></body></html>'

    save_rendered_page(html, output_dir=str(output_dir), static_src=str(static_src))

    index_file = output_dir / "index.html"
    copied_static = output_dir / "static" / "sdss-logo.png"

    assert index_file.exists()
    assert copied_static.exists()
    assert "./static/sdss-logo.png" in index_file.read_text(encoding="utf-8")


def test_build_flipper_end_to_end(tmp_path, monkeypatch, sample_package_root, sample_cfg):
    from flipper import build as b

    monkeypatch.chdir(tmp_path)

    @contextmanager
    def fake_as_file(_):
        yield sample_package_root

    monkeypatch.setattr(b.resources, "files", lambda package: sample_package_root)
    monkeypatch.setattr(b.resources, "as_file", fake_as_file)
    monkeypatch.setattr(b, "resolve_release", lambda request_release, environ_release=None: "dr19")

    def fake_load():
        b.config.cfg = copy.deepcopy(sample_cfg)

    monkeypatch.setattr(b.config, "load", fake_load)

    b.build_flipper()

    index_file = tmp_path / "deploy" / "index.html"
    copied_static = tmp_path / "deploy" / "static" / "sdss-logo.png"

    assert index_file.exists()
    assert copied_static.exists()

    html = index_file.read_text(encoding="utf-8")
    assert "SDSS Splashpage" in html
    assert "https://dr19.sdss.org/infrared/" in html
    assert "./static/sdss-logo.png" in html

def test_build_flipper_dev_mode(tmp_path, monkeypatch, sample_package_root, sample_cfg):
    from flipper import build as b
    from contextlib import contextmanager
    import copy

    monkeypatch.chdir(tmp_path)

    @contextmanager
    def fake_as_file(_):
        yield sample_package_root

    monkeypatch.setattr(b.resources, "files", lambda package: sample_package_root)
    monkeypatch.setattr(b.resources, "as_file", fake_as_file)
    monkeypatch.setattr(b, "resolve_release", lambda request_release, environ_release=None: "dr19")

    # Make dr19 valid
    b.config.available_releases = ["dr19", "dr20"]

    # Add dev config into YAML
    dev_cfg = copy.deepcopy(sample_cfg)
    dev_cfg["dev"] = {
        "wordpress_url": "testng.sdss.org",
        "skyserver_release": ""
    }

    def fake_load():
        b.config.cfg = dev_cfg

    monkeypatch.setattr(b.config, "load", fake_load)

    # 👇 run with dev=True
    b.build_flipper(dev=True)

    html = (tmp_path / "deploy" / "index.html").read_text(encoding="utf-8")

    # WordPress links should now use dev URL
    assert "https://testng.sdss.org/news/" in html

    # Skyserver should NOT include /dr19 anymore
    assert "https://skyserver.sdss.org/" in html
    assert "https://skyserver.sdss.org/dr19" not in html

def test_build_flipper_skyserver_no_release(tmp_path, monkeypatch, sample_package_root, sample_cfg):
    from flipper import build as b
    from contextlib import contextmanager
    import copy

    monkeypatch.chdir(tmp_path)

    @contextmanager
    def fake_as_file(_):
        yield sample_package_root

    monkeypatch.setattr(b.resources, "files", lambda package: sample_package_root)
    monkeypatch.setattr(b.resources, "as_file", fake_as_file)
    monkeypatch.setattr(b, "resolve_release", lambda request_release, environ_release=None: "dr19")

    b.config.available_releases = ["dr19", "dr20"]

    def fake_load():
        b.config.cfg = copy.deepcopy(sample_cfg)

    monkeypatch.setattr(b.config, "load", fake_load)

    b.build_flipper(skyserver_no_release=True)

    html = (tmp_path / "deploy" / "index.html").read_text(encoding="utf-8")

    assert "https://skyserver.sdss.org/" in html
    assert "https://skyserver.sdss.org/dr19" not in html

def test_build_flipper_mirror_none_keeps_primary_release_urls(tmp_path, monkeypatch, sample_package_root, sample_cfg):
    from flipper import build as b
    from contextlib import contextmanager
    import copy

    monkeypatch.chdir(tmp_path)

    @contextmanager
    def fake_as_file(_):
        yield sample_package_root

    monkeypatch.setattr(b.resources, "files", lambda package: sample_package_root)
    monkeypatch.setattr(b.resources, "as_file", fake_as_file)
    monkeypatch.setattr(b, "resolve_release", lambda request_release, environ_release=None: "dr19")

    b.config.available_releases = ["dr19", "dr20"]

    def fake_load():
        b.config.cfg = copy.deepcopy(sample_cfg)

    monkeypatch.setattr(b.config, "load", fake_load)

    b.build_flipper(mirror=None)

    html = (tmp_path / "deploy" / "index.html").read_text(encoding="utf-8")

    assert "https://dr19.sdss.org/infrared/" in html
    assert "https://dr19.sdss.org/sas/" in html
    assert "https://dr20.sdss.org/sas/" not in html

def test_wordpress_use_release_false_does_not_prefix_release(sample_cfg):
    from flipper.index import load_sections_from_yaml
    from flipper.Config import config
    import copy

    cfg = copy.deepcopy(sample_cfg)

    # mimic sdsshome card
    cfg["sections"] = [
        {
            "rows": [
                {
                    "cards": [
                        {
                            "title": "SDSS Home",
                            "use_wordpress": True,
                            "use_release": False,
                            "url": "/",
                        }
                    ]
                }
            ]
        }
    ]

    config.release = "dr20"
    config.cfg = cfg

    sections = load_sections_from_yaml()
    card = sections[0]["rows"][0]["cards"][0]

    assert card["href"] == "https://www.sdss.org/"

def test_wordpress_use_release_true_prefixes_release(sample_cfg):
    from flipper.index import load_sections_from_yaml
    from flipper.Config import config
    import copy

    cfg = copy.deepcopy(sample_cfg)

    # mimic lvmvis/tutorials cards
    cfg["sections"] = [
        {
            "rows": [
                {
                    "cards": [
                        {
                            "title": "LVM",
                            "use_wordpress": True,
                            "use_release": True,
                            "url": "/lvm/getting_started/",
                        }
                    ]
                }
            ]
        }
    ]

    config.release = "dr20"
    config.cfg = cfg

    sections = load_sections_from_yaml()
    card = sections[0]["rows"][0]["cards"][0]

    assert card["href"] == "https://www.sdss.org/dr20/lvm/getting_started/"

def test_external_urls_are_preserved(sample_cfg):
    from flipper.index import load_sections_from_yaml
    from flipper.Config import config
    import copy

    cfg = copy.deepcopy(sample_cfg)

    cfg["sections"] = [
        {
            "rows": [
                {
                    "cards": [
                        {
                            "title": "Voyages",
                            "external_url": "http://voyages.sdss.org",
                        },
                        {
                            "title": "With Release",
                            "external_url": "https://example.com/{{release}}/docs",
                        },
                    ]
                }
            ]
        }
    ]

    config.release = "dr20"
    config.cfg = cfg

    sections = load_sections_from_yaml()
    cards = sections[0]["rows"][0]["cards"]

    assert cards[0]["href"] == "http://voyages.sdss.org"
    assert cards[1]["href"] == "https://example.com/dr20/docs"