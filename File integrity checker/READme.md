# File intergrity checker

This is a python file built by Boaz Amakye Adjei to check the file integrity of files on a pc.
It is a command line tool for check for the integrity of files.
It uses and excel database to store the generated file hash

### Python Modules used

- os
- hashlib
- pandas
- colorama
- argparse
- datatime

### How it works

- -a, --add: To generate and add the file hashes to the database
- -c, --check: To check and compare the file hash in the database to see if the file have been modified
- -h, --help: To bring the help menu

> example command
> python file-integrity-checker.py C:\\path\to\file --add

1. First, the user supplies the path of the file or directory and adds the flags -a to add or -c to check
2. If -a/--add is used the file's name, hash, size, alogrithm, file path, date added will be added to the database
3. If -c/--check is used, it will generate the file hash and compare it with the one in the database to see if it matches and give out the result
4. If --help is used, it will show the help menu
