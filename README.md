# dupecheck
Duplicate File checker - test project

## Description
This project has been refactored back down to a single command, dupecheck. This utility is the general purpose routine for creating an initial file database, updating that database (adding new file data, updating existing data, and/or deleting data), and running checks on the contents of a specified directory tree to see if there are any possible duplicates in the existing database.

There is now a command-line argument which specifies what action to take. These are:

create - Create a new file info database, and seed it with initial data from the supplied directory tree. If the file already exists, the process will abort with an error. Otherwise, the file will be created as a file info database (a SQLLite database).

check - using an existing file info database, compare the contents of the specified directory tree and display any possible matches (by file size and by file name). Will also indicate if no matches are found.

update - will update the specified file info database information that pertains to the specified directory tree to exactly reflect what the current state is. This means new files will be added, existing files will be checked and have their file size updated, and deleted files will be removed from the database.

If no command line arguments are passed, the utility will respond with a help screen.

## Usage
The command line arguments are:

```dupecheck.py  command  database_file  directory_tree```

### Examples:

```dupecheck.py  create  /files.db  /file/system```

If /files.db exists, will exit with an error. Otherwise, will create /files.db as a database file, and will populate it with information from the tree /file/system

```dupecheck.py  check  /my/files.db  /my/file/system```

Will walk the tree /my/file/system and compare the contents to information in the file info database /my/files.db. Any possible matches by file size or file name will be called out, or else the fact no matches were found will be displayed.

```dupecheck.py  update  /some/files.db  /another/filesystem```

Will update the file info database /some/files.db information to reflect the current state of directory tree /another/filesystem. Any info not in the database will be added, any existing info will be compared and udpated if necessary, and anything in the database that is not in the filesystem will be removed from the database.

## Requirements:

These routines were written in, and intended for, Python version 3.6.3 or higher. There are some functions and formats that will not work in prior versions of Python.

The current implementation requires no external libraries. Only internal libraries were used, including SQLlite.

The requirements.txt file was generated from a pip freeze command, just to be sure. The empty requirements file is not an error or oversight.
