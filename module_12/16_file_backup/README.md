# File Backup Utility

## Project Overview
`backup_files.py` copies all files from the `source` directory to a `backup` directory. Existing files are overwritten so that the backup always mirrors the source.

## Variables
`SOURCE_DIR` and `BACKUP_DIR` define the directories used for the operation. They default to `source` and `backup` subfolders.

## Instructions
Ensure `shutil` is available (it is part of the standard library). Place files in the `source` directory and run `python backup_files.py` to copy them to `backup`.

## Explanation
The script iterates through files in the source folder and uses `shutil.copy2` to preserve metadata during the copy. It creates the backup folder if it does not exist, providing a lightweight replication tool.
