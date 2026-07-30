import argparse

from flipper.build import build_flipper
from flipper.create_snaps import create_snaps

def cli():
    parser = argparse.ArgumentParser(
        description='Script to build Flipper',
        epilog="""
Examples:
  %(prog)s -r dr20                           # Release version for deployment
  %(prog)s -tr dr20 -c work -o deploy_testng # Pre-Release Proprietary testing end
  %(prog)s -r data -c work                   # For deployment to non-DR url (eg data.sdss5.org)
""", formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-r', '--release', help='Manually Set release', type=str, default=None)
    parser.add_argument('-c', '--config', help='Config File Release (defaults to {release}.yaml)', type=str, default=None)
    parser.add_argument('-t', '--dev', help='Use testng base url for wordpress', 
                        action='store_true', default=False)
    parser.add_argument('-j', '--skyserver', help='Use SkyServer without release',
                        action='store_true', default=False, dest='skyserver_no_release')
    parser.add_argument('-m', '--mirror', help='Use mirror url (e.g. dev-mirror for dev-mirror.sdss.org)', type=str, default=None)
    parser.add_argument('-o', '--outdir', default='./deploy', help='Output directory for static deployment')

    args = parser.parse_args()

    if args.config is None:
        args.config = args.release
    build_flipper(args.release, dev=args.dev, skyserver_no_release=args.skyserver_no_release,
                   mirror=args.mirror, outdir = args.outdir, config_release = args.config)

def cli_create_snaps():
    parser = argparse.ArgumentParser(
        description='Script to build Flipper Snapshot icons',
        epilog="""
Examples:
  %(prog)s --release 20 
        # Set the Release String in Zora and SkyServer Snapshots 
  %(prog)s --banner 'NEW: "Ancient Immigrant" star puzzles, delights astronomers' --release 20
        # Set the Banner at the top of sdss wordpress HTML page, and the release string elsewhere
""", formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--yaml', default=None, help='Path to YAML file containing snapshot configurations')
    parser.add_argument('--outdir', default=None, help='Output directory for snapshot images')
    parser.add_argument('--release', default = None, help='Release value to replace in sites (eg 20)')
    parser.add_argument('--banner', default=None, help='New SDSS Banner Text')

    args = parser.parse_args()
    create_snaps(yaml_path=args.yaml, outdir=args.outdir)

if __name__ == "__main__":
    cli()

