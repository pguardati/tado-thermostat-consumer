import os
import click

from src.cli.extract_and_process_thermostat import LAKE_DIR
from src.stages.backup import LocalBackup

TARGET_DIR = os.path.join(LAKE_DIR, "staging")
BACKUP_DIR = os.path.join(LAKE_DIR, "backups")


@click.command()
@click.argument(
    "target_dir",
    default=TARGET_DIR,
)
@click.option(
    "--backup-dir",
    "-b",
    default=BACKUP_DIR,
)
def create_backup(target_dir, backup_dir):
    backup_system = LocalBackup(target_dir, backup_dir)

    try:
        backup_system.create_new()
        last_backup = backup_system.get_last_backup()

        if last_backup:
            index, backup_path = last_backup
            click.echo(f"Backup #{index} created successfully at '{backup_path}'.")

        else:
            click.echo("Backup was created, but could not retrieve backup details.")

    except Exception as e:
        click.echo(f"An error occurred while creating the backup: {e}", err=True)


if __name__ == "__main__":
    create_backup()
