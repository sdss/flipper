import argparse

from flipper.build import build_flipper
from flipper.create_snaps import create_snaps

def cli():
    parser = argparse.ArgumentParser(description='Script to build Flipper')
    parser.add_argument('-r', '--release', help='Manually Set release', type=str, default=None)
    parser.add_argument('-t', '--dev', help='Use testng base url for wordpress', 
                        action='store_true', default=False)
    parser.add_argument('-j', '--skyserver', help='Use SkyServer without release',
                        action='store_true', default=False, dest='skyserver_no_release')
    parser.add_argument('-m', '--mirror', help='Use mirror url (e.g. dev-mirror for dev-mirror.sdss.org)', type=str, default=None)
    args = parser.parse_args()

    build_flipper(args.release, dev=args.dev, skyserver_no_release=args.skyserver_no_release, mirror=args.mirror)

def cli_create_snaps():
    parser = argparse.ArgumentParser(description='Script to build Flipper Snapshot icons')
    parser.add_argument('--yaml', default=None, help='Path to YAML file containing snapshot configurations')
    parser.add_argument('--outdir', default=None, help='Output directory for snapshot images')
    args = parser.parse_args()
    create_snaps(yaml_path=args.yaml, outdir=args.outdir)

if __name__ == "__main__":
    cli()

