# dupefind
Duplicate File finder - test project

This routine will do a treewalk on a specified path, and look for potential duplicate files. It
makes two separate comparisons, first by file size matches, and then a second pass using file name
matches (using only the file name, excluding the directory path portion). Each pass is an "OR"
operation. Each pass outputs the potential candidates separately.

The routine uses a database to build and store the fileysstem information used in the comparisons.
Then queries are run with specific criteria to help determine potential matches.

At the end, the routine will output all match candidates to stdout. The user can redirect the
output to a file, and then use that as a list for additional comparison.


REQUIREMENTS:

This routine was written in, and intended for, Python 3. There are some functions and formats that
will not work in prior versions of Python.

The current (first) version requires no external libraries. Only internal libraries were used,
including SQLlite.

The requirements.txt file was generated from a pip freeze command, just to be sure. The empty
requirements file is not an error or oversight.
