import os
import shutil
import datetime
import click

from src.extract_and_process_thermostat import LAKE_DIR

TARGET_DIR = os.path.join(LAKE_DIR, "staging")
BACKUP_DIR = os.path.join(LAKE_DIR, "backups")


@click.command()
@click.argument(
    "target_dir",
    default=TARGET_DIR,
    type=click.Path(exists=True, file_okay=False, readable=True),
)
@click.option(
    "--backup-dir",
    "-b",
    default=BACKUP_DIR,
    show_default=True,
    type=click.Path(file_okay=False, writable=True),
)
def create_backup(target_dir, backup_dir):
    # Convert paths to absolute paths
    target_dir = os.path.abspath(target_dir)
    backup_dir = os.path.abspath(backup_dir)

    # Ensure the backup directory exists
    try:
        os.makedirs(backup_dir, exist_ok=True)
    except Exception as e:
        click.echo(f"Error creating backup directory '{backup_dir}': {e}", err=True)
        return

    # Copy the target directory to the backup location
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    backup_path = os.path.join(backup_dir, backup_name)
    try:
        #
        shutil.copytree(target_dir, backup_path)
        click.echo(f"Backup created successfully at '{backup_path}'.")
    except Exception as e:
        click.echo(f"An error occurred while creating the backup: {e}", err=True)


if __name__ == "__main__":
    create_backup()
