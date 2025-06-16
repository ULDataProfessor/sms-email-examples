# File Organization Automation

## Project Overview
This script groups files in your Downloads directory into folders based on file extension. By cleaning up the folder automatically, it prevents clutter and makes it easier to locate documents, images, and other resources.

## Variables
The main configuration is `EXTENSION_MAP` inside `organize_downloads.py`. It maps extensions such as `.txt` or `.pdf` to subdirectory names. The script also accepts an optional path to override the default `~/Downloads` location.

## Instructions
Run `python organize_downloads.py` from this directory. New folders will be created for each extension listed in `EXTENSION_MAP` and matching files will be moved into them. Logs are printed to the console for every file processed.

## Explanation
`organize_downloads` iterates through each item in the source folder using `pathlib.Path`. For every file it checks the extension and moves it to the corresponding subfolder with `shutil.move`. By customizing `EXTENSION_MAP` you can easily extend the behavior to support additional file types.
