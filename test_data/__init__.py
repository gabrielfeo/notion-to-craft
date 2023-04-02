from pathlib import Path
import filecmp
import io
from contextlib import redirect_stdout
import textwrap
import subprocess
from dataclasses import dataclass
from collections import namedtuple

filecmp.DEFAULT_IGNORES.append('.DS_Store')


@dataclass
class TestDataDir:
    name: str
    input: Path
    expected_output: Path


dirs: dict[str, TestDataDir] = {}

for path in Path(__file__).parent.glob('*'):
    if path.is_dir():
        dirs[path.name] = TestDataDir(name=path.name,
                                      input=path/'input',
                                      expected_output=path/'output')


def assert_dir_content_equals(a, b):
    with redirect_stdout(io.StringIO()) as out:
        filecmp.dircmp(a, b).report_full_closure()
        report = out.getvalue()
        if 'Only in' in report or 'Differing' in report:
            report = textwrap.indent(report, '  ')
            diff = subprocess.run(['diff', '-ru', a, b],
                                  capture_output=True).stdout
            diff = textwrap.indent(diff.decode(), '  ')
            msg = f"Not equal: '{a}' and '{b}'. filecmp:\n{report}\n\n  diff:\n{diff}"
            raise AssertionError(msg)
