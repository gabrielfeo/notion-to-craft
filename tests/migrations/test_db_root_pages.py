from notion_to_craft.migrations import migrate_db_root_pages
from tempfile import TemporaryDirectory
import unittest
import test_data
from pathlib import Path


data_dir = test_data.dirs['test_db_root_pages']


class TestMigrateDbRootPages(unittest.TestCase):

    def setUp(self):
        self.output_dir = Path(TemporaryDirectory().name)

    def test_migrate_db_root_pages(self):
        migrate_db_root_pages(data_dir.input, self.output_dir)
        test_data.assert_dir_content_equals(data_dir.expected_output,
                                            self.output_dir)
