import os
import yaml
from importlib import resources
from pathlib import Path
from datetime import date
import logging

class Config:
    def __init__(self, base=None,  release=None, dev=False, skyserver_no_release=False, mirror=False):
        self.base = base or os.environ.get("FLIPPER_BASE", "flipper")
        self.release = release
        self.available_releases = self.get_available_releases()
        self.dev = dev
        self.skyserver_no_release = skyserver_no_release
        self.cfg = None  # This will hold the loaded YAML config sections
        self.copyright_year = date.today().year
        self.mirror = mirror

    def get_available_releases(self):
        config_dir = resources.files("flipper.config")
        releases = []
        for file in config_dir.iterdir():
            if file.name.startswith("dr") and file.name.endswith(".yaml"):
                releases.append(file.name.removesuffix(".yaml"))
        return releases

    def set_release(self, release=None, dev=False, skyserver_no_release=False, mirror=None):
        self.release = release or os.environ.get("FLIPPER_RELEASE")
        if self.release is not None:
            if self.release not in self.available_releases:
                logging.warning(f"Release '{self.release}' not found in available releases: {self.available_releases}. Defaulting to latest release's template.")
                sorted_rels = sorted(self.available_releases, key=lambda x: int(x.split("dr")[-1]))
                self.release = sorted_rels[-1]
        self.dev = dev
        self.skyserver_no_release = skyserver_no_release
        self.mirror = mirror
            
    def set_wordpress_url(self):
        if self.cfg is None:
            self.load()
        if self.dev:
            self.cfg['wordpress_url'] = self.cfg.get('dev', {}).get('wordpress_url', 'https://testng.sdss.org')
            self.cfg['skyserver_release'] = self.cfg.get('dev', {}).get('skyserver_release', '')
        else:
            self.cfg['wordpress_url'] = self.cfg.get('wordpress_url', 'https://www.sdss.org')
            self.cfg['skyserver_release'] = self.cfg.get('skyserver_release', '')
        if self.skyserver_no_release:
            self.cfg['skyserver_release'] = ''

    def load(self):
        config_dir = resources.files("flipper.config")
        yaml_path = (config_dir / self.release).with_suffix(".yaml")

        try:
            with yaml_path.open("r", encoding="utf-8") as f:
                self.cfg = yaml.safe_load(f)
        except Exception as exc:
                raise RuntimeError(
                    f"Failed to load YAML from file '{yaml_path }': {exc}"
                )
        
config = Config()

