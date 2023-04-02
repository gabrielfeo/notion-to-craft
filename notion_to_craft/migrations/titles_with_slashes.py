import os
import shutil
import csv
import urllib.parse
from pathlib import Path
from collections import namedtuple
from dataclasses import dataclass


@dataclass
class Replace:
    exported_path: Path
    original_name: str
    content: str

    def __post_init__(self):
        self.exported_name = self.original_name.replace('/', ' ')
        self.new_name = self.original_name.replace('/', '-')
        new_filename = self.exported_path.name.replace(self.exported_name,
                                                       self.new_name)
        self.new_path = self.exported_path.parent / new_filename
        self.exported_link = f"[{self.exported_name}]"


def migrate_titles_with_slashes(input_dir: Path, output_dir: Path):
    """
    Notion replaces slashes in page titles with spaces, but leaves titles with
    slashes in database content (both csv and child md page). This replaces
    spaces in filenames with a hyphen instead, which is best for dates, and
    does the same in the page's H1 heading and the page's name in the database
    content CSV.

    Before: a page '2023/01/02 Foo/bar' is exported as a file '2023 01 02
            Foo bar', with heading '2023/01/02 Foo/bar' and listed as
            '2023/01/02 Foo/bar' in database CSV.

    After:  a page '2023/01/02 Foo/var' is exported as a file '2023-01-02
            Foo-bar', with heading '2023-01-02 Foo-bar' and listed as
            '2023-01-02 Foo-bar' in database CSV.

    TODO Nested pages
    """
    shutil.copytree(input_dir, output_dir)
    replaces = []
    for path in output_dir.glob('**/*.md'):
        h1_heading, content = path.read_text().split('\n', 2)[0]
        original_page_name = h1_heading.split('#', 2)[1].strip()
        if '/' not in original_page_name:
            continue
        replaces.append(Replace(exported_path=path,
                                original_name=original_page_name,
                                content=content))
    # Replace links to pages first
    for page in output_dir.glob('**/*.md'):
        content = page.read_text()
        for  in page.read_text():

    # Replace filename and h1 heading
    for replace in replaces:
        replace.new_path.write_text(f"# {replace.new_name}\n{replace.content}")
        os.remove(replace.exported_path)
