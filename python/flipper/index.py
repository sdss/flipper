#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from flipper.Config import config

from typing import Optional, List, Dict, Any
from jinja2 import Environment

# def set_wordpress_url(dev: bool = False, skyserver_no_release: bool = False):
#     if dev:
#         config.cfg.wordpress_url = config.cfg.dev.wordpress_url
#         config.cfg.skyserver_release = config.cfg.dev.skyserver_release
#     if skyserver_no_release:
#         config.cfg.skyserver_release = ""


def resolve_release(
    request_release: Optional[str] = None,
    environ_release: Optional[str] = None,
) -> str:
    if request_release:
        return request_release
    if environ_release:
        return environ_release
    sorted_rels = sorted(config.available_releases, key=lambda x: int(x.split("dr")[-1]))
    return sorted_rels[-1]


def load_sections_from_yaml() -> List[Dict[str, Any]]:
    sections = config.cfg.get("sections", []) or []

    for section in sections:
        if "rows" not in section and "cards" in section:
            section["rows"] = [{"cards": section.pop("cards")}]

        section_rows = section.get("rows", []) or []
        section["rows"] = section_rows

        for row in section_rows:
            cards = row.get("cards", []) or []
            row["cards"] = cards

            for card in cards:
                href = "#"

                external = card.get("external_url")
                if external:
                    href = str(external)
                    if config.release:
                        href = href.replace("{{release}}", config.release)

                elif card.get("use_skyserver"):
                    if config.dev:
                        skyserver_release = config.dev_base.skyserver_release
                    else:
                        skyserver_release = config.base.skyserver_release
                    if skyserver_release:
                        href = f"https://skyserver.sdss.org/{skyserver_release}"
                    else:
                        href = "https://skyserver.sdss.org/"

                elif card.get("use_wordpress"):
                    href = None
                    if config.dev:
                        if not config.dev_base.wordpress_url:
                            href = "#"
                    else:
                        if not config.base.wordpress_url:
                            href = '#'
                    if href is None:
                        path = card.get("url", "/")
                        if not path.startswith("/"):
                            path = "/" + path
                        if card.get("use_release", False):
                            path = f"/{config.release}{path}"
                        if config.dev:
                            href = f"https://{config.dev_base.wordpress_url}{path}"
                        else:
                            href = f"https://{config.base.wordpress_url}{path}"

                elif card.get("url"):
                        
                    path = card.get("url", "/")
                    if not path.startswith("/"):
                        path = "/" + path
                    if config.dev:
                        tbase_host = config.dev_base.base_url
                    else:
                        tbase_host = config.base.base_url
                    if config.mirror is not None:
                        if card.get("mirror",None) is not None:
                            tbase_host = tbase_host.replace("{{release}}", config.mirror)
                            if card.get('picture', None):
                                card['picture'] = card.get('mirror')
    
                    tbase_host = tbase_host.replace("{{release}}", config.release)

                    href = f"https://{tbase_host}{path}"

                card["href"] = href

    return sections

