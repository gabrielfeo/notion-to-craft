import argparse
from . import migrations
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', '-i', required=True, type=Path, help='Root dir of original Notion export')
parser.add_argument('--output-dir', '-o', required=True, type=Path, help='Output dir')


def run(args=None):
    args = parser.parse_args(args)
    migrations.migrate_db_root_pages(input_dir=args.input_dir, output_dir=args.output_dir)
