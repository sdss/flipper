
import sys
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(
            "Playwright is not installed.\n"
            "Install dev dependencies with:\n\n"
            "    uv sync --group snap\n"
            "or\n"
            "    uv pip install playwright Pillow\n"
            )
    sys.exit(1)

from urllib.parse import urlparse
from PIL import Image
import yaml
import flipper
import os
import argparse

import netrc
# Load default ~/.netrc file
auth = netrc.netrc()

outdir = os.path.join(os.path.dirname(flipper.__file__),'static')
config_dir = os.path.join(os.path.dirname(flipper.__file__),'config')

def create_snaps(yaml_path= None, outdir=None):
    if yaml_path is None:
        yaml_path = os.path.join(config_dir, "snaps.yaml")
    if outdir is None:
        outdir = os.path.join(os.path.dirname(flipper.__file__),'static')
    # Load YAML from file
    with open(yaml_path, "r") as f:
        snaps = yaml.safe_load(f)

    for site in snaps:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                        headless=True,
                        args=["--force-device-scale-factor=2.5"]
                        )
            
                parsed = urlparse(site['url'])
                host=parsed.hostname
                credentials = auth.authenticators(host)
            
                if credentials:
                    context = browser.new_context(
                            viewport={"width": 1440, "height": 800},  # adjust height similarly
                            device_scale_factor=2.5,
                            http_credentials={
                                "username":credentials[0],
                                "password":credentials[2]
                                }
                            )
                else:
                    context = browser.new_context(
                            viewport={"width": 1440, "height": 800},  # adjust height similarly
                            device_scale_factor=2.5
                            )          
            
                page = context.new_page()
                page.goto(site['url'], wait_until="networkidle")
                page.screenshot(path=os.path.join(outdir,site['out']+'.png'))
        except Exception as e:
            if "Executable doesn't exist" in str(e) or "playwright install" in str(e):
                print(
                        "Playwright is installed but browsers are not downloaded.\n"
                        "Run:\n\n"
                        "    playwright install\n"
                        )
                sys.exit(1)
                raise
        with Image.open(os.path.join(outdir,site['out']+'.png')) as img:
            img.save(os.path.join(outdir,site['out']+'.webp'), "WEBP", quality=80)    
        print(f'Snapped {site["url"]} to {os.path.join(outdir,site["out"])}.webp')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to build Flipper Snapshot icons')
    parser.add_argument('--yaml', default=yaml_path, help='Path to YAML file containing snapshot configurations')
    parser.add_argument('--outdir', default=outdir, help='Output directory for snapshot images')
    args = parser.parse_args()
    create_snaps(yaml_path=args.yaml, outdir=args.outdir)