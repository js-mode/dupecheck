# dupefind
Duplicate File finder - test project

There are now two routines included in this project. Running a routine without passing it any
commandline parameters will bring up a help screen describing parameters and usage.


dupefind:
=========
This routine will do a treewalk on a specified path, and look for potential duplicate files. It
makes two separate comparisons, first by file size matches, and then a second pass using file name
matches (using only the file name, excluding the directory path portion). Each pass is an "OR"
operation. Each pass outputs the potential candidates separately.

The routine uses a database to build and store the filesystem information used in the comparisons.
Then queries are run with specific criteria to help determine potential matches.

At the end, the routine will output all match candidates to stdout. The user can redirect the
output to a file, and then use that as a list for additional comparison.

The database is left behind for future use by other utilities, such as dupecheck. The database file
is output to a predefined file path and location, which is specified in config.py as DB_FILE.
Today that is './filebase.db".


dupecheck:
==========
This routine will run through a given directory structure and alert the user (via output) to any
possible duplicate files in that directory structure, compared to an existing files database of some
other directory structure.

It can also be invoked to add the current directory structure files into the specified files
database. In that invocation, no duplicate checks are performed. The files are only added, but
only if the directory name and file name are not already in the database (i.e. no duplicate
inserts are performed).

The add mode is intended more as a second pass. First pass would be to run this utility to find and
validate/weed out any duplicates, and then do a second run to update the files database with the
new information.

Note that the utility will filter out the treewalk path from the match results. This allows the
utility to be run, or re-run, on a directory that is already in the files database structure. 


REQUIREMENTS:

These routines were written in, and intended for, Python 3. There are some functions and formats
that will not work in prior versions of Python.

The current (first) version requires no external libraries. Only internal libraries were used,
including SQLlite.

The requirements.txt file was generated from a pip freeze command, just to be sure. The empty
requirements file is not an error or oversight.
