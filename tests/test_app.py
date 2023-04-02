from notion_to_craft import app
from tempfile import TemporaryDirectory
import unittest
import test_data
from pathlib import Path


class TestApp(unittest.TestCase):

    def test_app(self):
        """Integration test of app and all migrations"""
        self.output_dir = Path(TemporaryDirectory().name)
        app.run(args=['--input-dir', str(test_data.original_export),
                      '--output-dir', str(self.output_dir)])
        expected_dir = test_data.expected_export / 'test_app'
        test_data.assert_dir_content_equals(expected_dir, self.output_dir)

    def test_parser_long_flags(self):
        app.parser.parse_args(args=['--input-dir', str(test_data.original_export),
                                    '--output-dir', str(test_data.original_export)])

    def test_parser_short_flags(self):
        app.parser.parse_args(args=['-i', str(test_data.original_export),
                                    '-o', str(test_data.original_export)])

    def test_parser_required_options(self):
        with self.assertRaises(SystemExit):
            app.parser.parse_args(args=['-i', str(test_data.original_export)])
        with self.assertRaises(SystemExit):
            app.parser.parse_args(args=['-o', str(test_data.original_export)])
