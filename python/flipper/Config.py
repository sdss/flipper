import os
import yaml
from importlib import resources
from pathlib import Path
from datetime import date
import logging

class Base:
    def __init__(self):
        self.wordpress_url = None
        self.skyserver_release = None
        self.base_url = None

class Config:
    def __init__(self, base=None, config = None, release=None, dev=False, skyserver_no_release=False, mirror=False):
        self.release = release
        self.config = config
        self.available_releases = self.get_available_releases()
        self.dev = dev
        self.skyserver_no_release = skyserver_no_release
        self.cfg = None  # This will hold the loaded YAML config sections
        self.copyright_year = date.today().year
        self.mirror = mirror
        self.base = Base()
        self.dev_base = Base()


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
            if (self.release not in self.available_releases) and (self.release not in ['data']):
                logging.warning(f"Release '{self.release}' not found in available releases: {self.available_releases}. Defaulting to latest release's template.")
                sorted_rels = sorted(self.available_releases, key=lambda x: int(x.split("dr")[-1]))
                self.release = sorted_rels[-1]
        self.dev = dev
        self.skyserver_no_release = skyserver_no_release
        self.mirror = mirror
            
    def set_wordpress_url(self):
        if self.cfg is None:
            self.load()
        self.dev_base.wordpress_url = self.cfg.get('dev', {}).get('wordpress_url', 'https://testng.sdss.org')
        self.dev_base.skyserver_release = self.cfg.get('dev', {}).get('skyserver_release', '')
        self.dev_base.base_url = self.cfg.get('dev',{}).get('base_url')

        self.base.wordpress_url = self.cfg.get('wordpress_url', 'https://www.sdss.org')
        self.base.skyserver_release = self.cfg.get('skyserver_release', '')
        self.base.base_url = self.cfg.get('base_url')
        if self.skyserver_no_release:
            self.dev_base.skyserver_release = ''
            self.base.skyserver_release = ''

    def load(self):
        config_dir = resources.files("flipper.config")
        config = self.config or self.release
        yaml_path = (config_dir / config).with_suffix(".yaml")
        print('test')
        try:
            with yaml_path.open("r", encoding="utf-8") as f:
                print(yaml_path)
                self.cfg = yaml.safe_load(f)
        except Exception as exc:
                raise RuntimeError(
                    f"Failed to load YAML from file '{yaml_path }': {exc}"
                )
        
config = Config()

