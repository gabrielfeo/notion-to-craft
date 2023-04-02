from notion_to_craft import app
from tempfile import TemporaryDirectory
import unittest
import test_data
from pathlib import Path


data_dir = test_data.dirs['test_app']

class TestApp(unittest.TestCase):

    def test_app(self):
        """Integration test of app and all migrations"""
        self.output_dir = Path(TemporaryDirectory().name)
        app.run(args=['--input-dir', str(data_dir.input),
                      '--output-dir', str(self.output_dir)])
        test_data.assert_dir_content_equals(data_dir.expected_output,
                                            self.output_dir)

    def test_parser_long_flags(self):
        app.parser.parse_args(args=['--input-dir', str(data_dir.input),
                                    '--output-dir', str(data_dir.input)])

    def test_parser_short_flags(self):
        app.parser.parse_args(args=['-i', str(data_dir.input),
                                    '-o', str(data_dir.input)])

    def test_parser_required_options(self):
        with self.assertRaises(SystemExit):
            app.parser.parse_args(args=['-i', str(data_dir.input)])
        with self.assertRaises(SystemExit):
            app.parser.parse_args(args=['-o', str(data_dir.input)])
