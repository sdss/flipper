#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import os
import shutil
from pathlib import Path
from typing import List, Dict, Any
from sdsstools import get_package_version
from importlib import resources

from jinja2 import Environment, FileSystemLoader, select_autoescape
from flipper.index import resolve_release, load_sections_from_yaml
from flipper.Config import config
__version__ = get_package_version(__file__, 'flipper')



def render_index(
    env: Environment,
    context: Dict[str, Any],
    sections: List[Dict[str, Any]],
    template_name: str = "index.html",
) -> str:
    def url_for(endpoint, **values):
        if endpoint == "static":
            return f"/static/{values['filename']}"
        if endpoint == "index.home":
            return "/"
        raise ValueError(f"Unknown endpoint: {endpoint}")

    env.globals["url_for"] = url_for
    template = env.get_template(template_name)
    return template.render(**context, sections=sections)



def create_env(template_dir="templates"):
    return Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )


def build_context() -> Dict[str, Any]:
    base_url = config.cfg.get('base_url', '').replace("{{release}}", config.release)

    wordpress_url = config.cfg.get('wordpress_url', '')
    skyserver_release = config.cfg.get('skyserver_release', '')
    return {
        "title": config.cfg.get('title', "SDSS Splashpage"),
        "version": __version__,
        "release": config.release,
        "base_url": base_url,
        "wordpress_url": wordpress_url,
        "skyserver_release": skyserver_release,
        "copyright_year": config.copyright_year,
    }

def save_rendered_page(html, output_dir="deploy", static_src="static"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    html = html.replace(f"/static/", f"./static/")

    index_path = output_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")
    print(f"Saved HTML to {index_path}")

    static_src = Path(static_src)
    static_dst = output_dir / "static"

    if static_src.exists():
        shutil.copytree(static_src, static_dst, dirs_exist_ok=True)
        print(f"Copied static files to {static_dst}")
    else:
        print("No static directory found to copy.")


def build_flipper(release = None, dev=False, skyserver_no_release=False, mirror=None):
    with resources.as_file(resources.files("flipper")) as flipper_path:
        env = create_env(template_dir= flipper_path / "templates")

        release = resolve_release(release, os.environ.get("FLIPPER_RELEASE"))

        config.set_release(release=release, dev=dev, skyserver_no_release=skyserver_no_release, 
                           mirror=mirror)
        config.load()
        config.set_wordpress_url()

        context = build_context()

        sections = load_sections_from_yaml()
        html = render_index(env, context, sections, template_name="index.html")
        save_rendered_page(html, output_dir="deploy", static_src=flipper_path / "static")

if __name__ == "__main__":
    build_flipper()