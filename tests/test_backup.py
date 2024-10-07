import os
import unittest
import tempfile

from src.stages.backup import LocalBackup


class TestLocalBackup(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for target and backup
        self.temp_dir = tempfile.TemporaryDirectory(dir=".")
        self.target_dir = os.path.join(self.temp_dir.name, "target")
        self.backup_dir = os.path.join(self.temp_dir.name, "backups")
        os.makedirs(self.target_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        # Initialize LocalBackup instance
        self.backup = LocalBackup(self.target_dir, self.backup_dir)
        # Create initial files in target directory
        with open(os.path.join(self.target_dir, "file1.txt"), "w") as f:
            f.write("This is file 1.")
        with open(os.path.join(self.target_dir, "file2.txt"), "w") as f:
            f.write("This is file 2.")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_new_backup(self):
        # Test creating a new backup
        self.backup.create_new()
        backups = self.backup.backups
        self.assertEqual(len(backups), 1, "There should be one backup after creation.")
        backup_path = backups[0]
        self.assertTrue(os.path.exists(backup_path), "Backup directory should exist.")
        # Check if files are copied
        file1 = os.path.join(backup_path, "file1.txt")
        file2 = os.path.join(backup_path, "file2.txt")
        self.assertTrue(os.path.isfile(file1), "file1.txt should exist in backup.")
        self.assertTrue(os.path.isfile(file2), "file2.txt should exist in backup.")

    def test_get_last_backup(self):
        # Test retrieving the last backup
        self.assertIsNone(
            self.backup.get_last_backup(), "Initially, there should be no backups."
        )
        self.backup.create_new()
        last_backup = self.backup.get_last_backup()
        self.assertIsNotNone(
            last_backup, "Last backup should not be None after creation."
        )
        index, backup_path = last_backup
        self.assertEqual(index, 1, "Backup index should be 1.")
        self.assertTrue(os.path.exists(backup_path), "Backup path should exist.")

    def test_restore_backup(self):
        # Test restoring from the last backup
        self.backup.create_new()
        # Modify the target directory
        os.remove(os.path.join(self.target_dir, "file1.txt"))
        with open(os.path.join(self.target_dir, "file3.txt"), "w") as f:
            f.write("This is file 3.")
        # Restore from backup
        success = self.backup.restore_backup()
        self.assertTrue(success, "Restore should be successful.")
        # Check if the target directory matches the backup
        file1 = os.path.join(self.target_dir, "file1.txt")
        file2 = os.path.join(self.target_dir, "file2.txt")
        file3 = os.path.join(self.target_dir, "file3.txt")
        self.assertTrue(os.path.isfile(file1), "file1.txt should exist after restore.")
        self.assertTrue(os.path.isfile(file2), "file2.txt should exist after restore.")
        self.assertFalse(
            os.path.exists(file3), "file3.txt should not exist after restore."
        )


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
