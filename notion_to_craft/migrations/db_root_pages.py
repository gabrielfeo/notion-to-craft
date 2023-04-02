import os
import shutil
import csv
import urllib.parse
from pathlib import Path


def migrate_db_root_pages(input_dir: Path, output_dir: Path):
    """
    Notion exports databases to CSV files, meaning there'll be no root page for
    a database in Craft. This replaces each CSV with a proper Markdown page
    describing the database's content pages.

    Before: a database is a csv listing child pages and their properties + a
            dir with child pages Markdown files
    After:  a database is a Markdown page with links to its child pages + a
            dir with child pages Markdown files

    Child pages themselves still contain their properties, even though the database page doesn't.
    """
    shutil.copytree(input_dir, output_dir)
    for path in output_dir.glob('**/*'):
        if path.suffix != '.csv':
            continue
        sibling_dirs = (p.name for p in path.parent.glob('*') if p.is_dir())
        if path.stem not in sibling_dirs:
            continue
        replace_database_csv_with_md_page(path)


def replace_database_csv_with_md_page(csv_path: Path):
    database_path = csv_path.parent / csv_path.stem
    child_names = child_names_from_csv(csv_path)
    child_links = build_child_links(database_path, child_names)
    write_database_page(database_path, child_links)
    os.remove(csv_path)


def child_names_from_csv(csv_path) -> list[str]:
    with open(csv_path, 'r') as csv_file:
        child_names = [row[0] for row in csv.reader(csv_file)]
        # Discard column header row
        return child_names[1:]


def build_child_links(database_path: Path, child_names: list[str]) -> list[str]:
    parent_dir = database_path.parent
    child_files = [p for p in database_path.glob('*') if p.is_file()]
    child_links = []
    for child_name in child_names:
        matching_pages = [f.name for f in child_files
                          if f.name.startswith(child_name)]
        assert len(matching_pages) == 1
        relative = database_path.relative_to(parent_dir) / matching_pages[0]
        relative_encoded = urllib.parse.quote(str(relative))
        child_links.append(f"[{child_name}]({relative_encoded})")
    return child_links


def write_database_page(database_path: Path, child_links: list[str]):
    md_path = f"{database_path}.md"
    with open(md_path, 'w') as md_file:
        database_name = database_path.name
        md_file.write(f"# {database_name}\n\n")
        md_file.writelines('\n\n'.join(child_links))
        md_file.write('\n')
