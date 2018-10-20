import os

from utils import db
from utils.functions import treewalk_with_action, is_file, is_dir, normalize_dir_name, print_matches
from utils.help import usage, help_create, help_check, help_update, help_report


class CommandException(Exception):
    """
    Basic exception class used for the commands.py module.
    Used to indicate a failure of some kind, and provide a string description for the failure
    """
    pass


def validate_general_params(parameters):
    """
    Validate the database file is a file, and the tree to walk is a directory
    This is a common use case for several commands, so centralizing validate into one routine
    Will raise an CommandException if there is an error
    :param parameters: the parameters passed in to validate. The general case is
    :                : first param is database file, and second param is the dir tree to walk
    :return first param: True if both are valid, otherwise raises a CommandException
    """
    dbfile = parameters[0]
    walkdir = parameters[1]
    if not is_file(dbfile):
        raise CommandException(f"{dbfile} is not a file, does not exist, or is not accessible")
    
    if not is_dir(walkdir):
        raise CommandException(f"{walkdir} is not a directory, does not exist, or is not accessible")
    
    return True


def create(parameters):
    """
    Create the database file, and then execute an update on it
    :param parameters: a list of the parameters passed in to this command from the command line.
    :                : the utiility (argv[0]) and the command itself (argv[1]) have already been
    :                : sripped, leaving only the parameters for the command itself.
    :return: nothing
    """
    if len(parameters) != 2:
        help_create()
        return

    dbfilename = parameters[0]
    dir_to_walk = normalize_dir_name(parameters[1])

    if is_file(dbfilename):
        print(f"\nError: file {dbfilename} already exists. Will not create database file on top of it.\n")
        return
    
    if not is_dir(dir_to_walk):
        print(f"\nError: {dir_to_walk} is not a directory, does not exist, or is not accessible.")
        return
    
    file_db = db.FileDatabase(dbfilename)
    file_db.cleanup()

    # now that the database is initialized, use update command method to populate the new database
    update(parameters)


def check(parameters):
    """
    Check a directory against the database, looking for possible duplicates
    :param parameters: a list of the parameters passed in to this command from the command line.
    :                : the utiility (argv[0]) and the command itself (argv[1]) have already been
    :                : sripped, leaving only the parameters for the command itself.
    :return: nothing    
    """

    if len(parameters) != 2:
        help_check()
        return

    try:
        validate_general_params(parameters)
    except CommandException as err:
        print(f"\nError: {err}\n")
        return

    dbfilename = parameters[0]
    dir_to_walk = normalize_dir_name(parameters[1])

    file_db = db.FileDatabase(dbfilename)
    state = dict()
    state['tot_matches'] = 0
    state['tot_size_matches'] = 0
    state['tot_name_matches'] = 0

    return_state = treewalk_with_action(file_db, dir_to_walk, [".DS_Store"], check_helper, \
                                        in_state = state)
    
    if state['tot_matches'] == 0:
        print("\nNo duplicates found.\n")
        return
    
    tot_matches = return_state['tot_matches']
    tot_size_matches = return_state['tot_size_matches']
    tot_name_matches = return_state['tot_name_matches']
    print(f"\nTotal possible matches found: {tot_matches:,}")
    print(f"Size matches: {tot_size_matches:,}")
    print(f"Name matches: {tot_name_matches:,}\n")


def check_helper(file_db, dir, fname, filesize, state):
    """
    This is the check() helper function that is executed inside the treewalk_with_action
    It will compare each found file with the database to see if there are any possible matches,
    and if so, will display those.
    :param file_db: the FileDatabase object for the connected database containing the file data
    :          dir: the directory the treewalk is currently in
    ;        fname: the specific file the treewalk is currently at
    :     filesize: the current (e.g. up-to-date) size of the file
    ;        state: a dictionary that can be used to store state info needed through the entire
    :             : treewalk run
    :return: Nothing. All results are either output via print, or stored in the state dictionary
    """
    full_file_name = os.path.join(dir, fname)
   
    result = file_db.find_files_of_size(filesize)
    found = 0
    if result:
        for match in result:
            if match[0] == dir and match[1] == fname:
                continue
            found += 1
            if found == 1:
                print(f"{full_file_name}: possible matches file size:")	
            state['tot_matches'] += 1
            state['tot_size_matches'] += 1
            target_fname = os.path.join(match[0], match[1])
            print(f"\t{target_fname}")
        if found:
            print("\n")

    result = file_db.find_files_of_name(fname)
    found = 0
    if result:
        for match in result:
            if match[0] == dir and match[1] == fname:
                continue
            found += 1
            if found == 1:
                print(f"{full_file_name}: possible matches file name:")
            state['tot_matches'] += 1
            state['tot_name_matches'] += 1
            target_fname = os.path.join(match[0], match[1])
            print(f"\t{target_fname}")
        if found:
            print("\n")
    
    return state


def update(parameters):
    """
    Update the file database with the info from the filesystem tree. This means adding missing
    file data, updating existing file data, and removing missing files from the database.
    :param parameters: a list of the parameters passed in to this command from the command line.
    :                : the utiility (argv[0]) and the command itself (argv[1]) have already been
    :                : sripped, leaving only the parameters for the command itself.
    :return: nothing   
    """

    if len(parameters) != 2:
        help_update()
        return
    try:
        validate_general_params(parameters)
    except CommandException as err:
        print(f"\nError: {err}\n")
        return 

    dbfilename = parameters[0]
    dir_to_walk = normalize_dir_name(parameters[1])

    state = dict()
    file_db = db.FileDatabase(dbfilename)

    # first, check existing data in the database
    # remove any files that are in the database, but not in the filesystem
    delete_missing_files(file_db, dir_to_walk, state)

    # helper has to do all the individual file work
    # so it has to do adds and updates
    return_state = treewalk_with_action(file_db, dir_to_walk, [".DS_Store"], update_helper, in_state=state)

    total = return_state.get('total', 0)
    skipped = return_state.get('skipped',0)
    added = return_state.get('added', 0)
    updated = return_state.get('updated', 0)
    deleted = return_state.get('deleted', 0)

    print(f"\nTotal files: {total:,}")
    print(f"\nSkipped: {skipped:,}")
    print(f"Added: {added:,}")
    print(f"Updated: {updated:,}")
    print(f"\nDeleted: {deleted:,}\n")


def delete_missing_files(file_db, dir_to_walk, state):
    """
    This function will take a file database and a starting directory, and will walk through the files in
    the database for that directory and all sub directories, and remove any files that no longer exist.
    :param file_db: the file database to use as the source
    :  dir_to_walk: the starting path, top level, to start checking if the files exist
    :        state: a dictionary that can be used to store state info and return data
    """

    # first walk the files in the specified directory
    # this is necessary due to the way the data is stored (without trailing os.sep)
    files_in_db = file_db.find_files_in_dir(dir_to_walk)
    for file in files_in_db:
        file_dir = file[0]
        file_name = file[1]
        full_file = os.path.join(file_dir, file_name)
        if not os.path.isfile(full_file):
            # remove from database
            file_db.delete(file_dir, file_name)
            state['deleted'] = state.get('deleted',0) + 1
            print(f"DELETED: {full_file}")

    # then walk through any and all sub directories under the given path
    files_in_db = file_db.find_files_below_dir(dir_to_walk)
    for file in files_in_db:
        file_dir = file[0]
        file_name = file[1]
        full_file = os.path.join(file_dir, file_name)
        if not os.path.isfile(full_file):
            # remove from database
            file_db.delete(file_dir, file_name)
            state['deleted'] = state.get('deleted',0) + 1
            print(f"DELETED: {full_file}")


def update_helper(file_db, dir, fname, filesize, state):
    """
    This is the update() helper function that is executed inside the treewalk_with_action
    It performs all the checks and actions necessary for the update function, during the treewalk
    This means looking for files to delete, add, and update or skip
    :param file_db: the FileDatabase object for the connected database containing the file data
    :          dir: the directory the treewalk is currently in
    ;        fname: the specific file the treewalk is currently at
    :     filesize: the current (e.g. up-to-date) size of the file
    ;        state: a dictionary that can be used to store state info needed through the entire
    :             : treewalk run
    :return: Nothing. All results are either output via print, or stored in the state dictionary
    """
    state['total'] = state.get('total',0) + 1
    full_fname = os.path.join(dir, fname)

    # add or update the file we are on right now
    result = file_db.find_specific_file(dir, fname)
    if not result:
        # add
        file_db.insert(dir, fname, filesize)
        state['added'] = state.get('added',0) + 1
        print(f"Added: {full_fname}")
        return

    # is update required?
    file_db_info = result[0]
    file_db_size = file_db_info[2]

    if file_db_size == filesize:
        #no update required
        state['skipped'] = state.get('skipped',0) + 1
        print(f"skipped: {full_fname}")
        return
    
    # update required
    file_db.update(dir, fname, filesize)
    state['updated'] = state.get('updated',0) + 1
    print(f"Updated: {full_fname}  old size = {file_db_size} new size = {filesize}")


def report(parameters):
    """
    Generate a report on possible duplicates inside the existing database.
    :param parameters: a list of the parameters passed in to this command from the command line.
    :                : the utiility (argv[0]) and the command itself (argv[1]) have already been
    :                : sripped, leaving only the parameters for the command itself.
    :return: nothing   
    """
    if len(parameters) == 0:
        help_report()
        return
    if len(parameters) > 1:
        try:
            min_size = int(parameters[1])
            min_size *= 1000
        except ValueError as err:
            print(f"Error: minimum size parameter: {err}")
            return
    else:
        min_size = None
    
    dbfilename = parameters[0]
    if not is_file(dbfilename):
        print(f"\nError: file {dbfilename} is not a file, does not exist, or is not accessible.\n")
        return
    
    file_db = db.FileDatabase(dbfilename)

    print_matches(file_db, min_size)
