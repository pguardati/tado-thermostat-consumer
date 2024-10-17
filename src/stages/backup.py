import os
import shutil
import datetime
from typing import List, Tuple, Optional


class LocalBackup:
    """
    A class to handle creating and restoring backups of a target directory.
    Backups are stored as subdirectories within the backup directory,
    each named with a timestamp indicating when the backup was created.
    """

    def __init__(self, target_dir: str, backup_dir: str):
        self.target_dir = os.path.abspath(target_dir)
        self.backup_dir = os.path.abspath(backup_dir)
        os.makedirs(self.backup_dir, exist_ok=True)
        self.backups = self._scan_backups()

    def _scan_backups(self) -> List[str]:
        backups = []
        for entry in os.listdir(self.backup_dir):
            backup_path = os.path.join(self.backup_dir, entry)
            if os.path.isdir(backup_path) and entry.startswith("backup_"):
                try:
                    # Validate backup directory name format
                    datetime.datetime.strptime(entry[7:], "%Y%m%d_%H%M%S")
                    backups.append(backup_path)
                except ValueError:
                    continue  # Ignore directories that don't match the format
        # Sort backups by datetime extracted from directory name
        backups.sort(
            key=lambda x: datetime.datetime.strptime(
                os.path.basename(x)[7:], "%Y%m%d_%H%M%S"
            )
        )
        return backups

    def create_new(self) -> None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        shutil.copytree(self.target_dir, backup_path)
        self.backups.append(backup_path)

    def get_last_backup(self) -> Optional[Tuple[int, str]]:
        if not self.backups:
            return None
        last_backup = self.backups[-1]
        index = len(self.backups)  # 1-based index
        return (index, last_backup)

    def restore_backup(self) -> bool:
        last_backup = self.get_last_backup()
        if not last_backup:
            print("No backups available to restore.")
            return False
        _, backup_path = last_backup
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)
        shutil.copytree(backup_path, self.target_dir)
        return True
