from notion_to_craft.migrations import migrate_db_root_pages
from tempfile import TemporaryDirectory
import unittest
import test_data
from pathlib import Path


class TestMigrateDbRootPages(unittest.TestCase):

    def setUp(self):
        self.output_dir = Path(TemporaryDirectory().name)

    def test_migrate_db_root_pages(self):
        migrate_db_root_pages(test_data.original_export, self.output_dir)
        expected_dir = test_data.expected_export / 'test_db_root_pages'
        test_data.assert_dir_content_equals(expected_dir, self.output_dir)
