from pathlib import Path
import filecmp
import io
from contextlib import redirect_stdout
import textwrap
import subprocess

filecmp.DEFAULT_IGNORES.append('.DS_Store')

original_export = Path(__file__).parent / 'original'
expected_export = Path(__file__).parent / 'expected'


def assert_dir_content_equals(a, b):
    with redirect_stdout(io.StringIO()) as out:
        filecmp.dircmp(a, b).report_full_closure()
        report = out.getvalue()
        if 'Only in' in report or 'Differing' in report:
            report = textwrap.indent(report, '  ')
            diff = subprocess.run(['diff', '-ru', a, b], capture_output=True).stdout
            diff = textwrap.indent(diff.decode(), '  ')
            msg = f"Not equal: '{a}' and '{b}'. filecmp:\n{report}\n\n  diff:\n{diff}"
            raise AssertionError(msg)
