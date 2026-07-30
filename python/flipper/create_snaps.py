
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
import os
import argparse

try:
    import flipper
    flipper_dir = flipper.__file__
except:
    flipper_dir = './'

import netrc
# Load default ~/.netrc file
auth = netrc.netrc()

outdir = os.path.join(os.path.dirname(flipper_dir),'static')
config_dir = os.path.join(os.path.dirname(flipper_dir),'config')

def create_snaps(yaml_path= None, outdir=None, release=None, banner=None):
    if yaml_path is None:
        yaml_path = os.path.join(config_dir, "snaps.yaml")
    if outdir is None:
        outdir = os.path.join(os.path.dirname(flipper_dir),'static')
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
                            viewport={"width": 1440, "height": 800}, 
                            device_scale_factor=2.5,
                            http_credentials={
                                "username":credentials[0],
                                "password":credentials[2]
                                }
                            )
                else:
                    context = browser.new_context(
                            viewport={"width": 1440, "height": 800}, 
                            device_scale_factor=2.5
                            )          
            
                page = context.new_page()
                if 'lvmvis' not in site['url']:
                    page.goto(site['url'], wait_until="networkidle")
                else:
                    page.goto(site['url'], wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_function("""() => document.querySelector('#aladin-div')""", timeout=60000)
                    page.wait_for_function("""
                            () => document.querySelector('#aladin-div .aladin-widgets-toolbar')
                            """, timeout=60000)
                    page.wait_for_function("""
                            () => {
                                const el = document.querySelector('#initial-loader');
                                if (!el) return true;
                                const s = getComputedStyle(el);
                                return s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0';
                            }
                            """, timeout=60000)
                    page.wait_for_function(
                                "() => document.querySelectorAll('[data-panel-id]').length > 0",
                                timeout=60000)
                    page.wait_for_timeout(2000)                    


                if banner:
                    topbar = page.locator('.site-topbar-text.site-topbar__left')
                    if topbar.count() > 0:
                        topbar.evaluate("(el, txt) => { el.textContent = txt; }", banner)

                if release: #Zora and SkyServer
                    btn = page.locator('#dselectdr')
                    if btn.count() > 0:
                        btn.evaluate("""
                        (el, rel) => {
                            const caret = el.querySelector('.caret');
                            el.childNodes.forEach(node => {
                                if (node.nodeType === Node.TEXT_NODE) {
                                    node.textContent = node.textContent.replace(/\\d+/, rel);
                                }
                            });
                        }
                        """, str(release))

                    inp = page.locator('#release')
                    if inp.count() > 0:
                        inp.fill(f'DR{release}')

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

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Script to build Flipper Snapshot icons')
#     parser.add_argument('--yaml', default=None, help='Path to YAML file containing snapshot configurations')
#     parser.add_argument('--outdir', default=None, help='Output directory for snapshot images')
#     parser.add_argument('--release', default = None, help='Release value to replace in sites (eg 20)')
#     parser.add_argument('--banner', default=None, help='New SDSS Banner Text')
#     args = parser.parse_args()
#     create_snaps(yaml_path=args.yaml, outdir=args.outdir, release= args.release, banner=args.banner)