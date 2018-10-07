import sys

command_name = sys.argv[0]

def usage():
    print(f"\n\n{command_name}  command  (additional parameters)")
    print("\nCommands:")
    print("\ncreate - Create the database (i.e. it does not already exist). If the database file does")
    print("         already exist, then the process will abort with an error. Otherwise, the database")
    print("         file will be created and processing will proceed as if an update command had given")
    print("         on an existing database file.")
    print("\ncheck  - Check the specified directory for duplicate entries in the file database, and")
    print("         display any potential matches for review.")
    print("\nupdate - Will modify the database entries for this directory to match the directory")
    print("         specified. NOTE that this will mean adding new files, updating stats on existing")
    print("         existing files, and removal of files in the database that are not in the filesystem.")
    print("\nEach command takes its own set of parameters. To see help for a specific command, run")
    print(f"\n{command_name} command")
    print("\nwith no parameters after the command.")
    print("")


def help_create():
    print(f"\n{command_name}  create  database_file  directory_to_check\n")
    print("database_file - required      - the path and filename of the files database to create")
    print("                                and then populate with initial data.")
    print("directory_to_check - required - the directory to walk, to populate the file database with.")
    print("\nExample:")
    print(f"\n{command_name} create /files.db /file/system\n")
    print("\tWill create the database files.db (or will abort with an error if that database file")
    print("\talready exists). Then will perform like an update command, which means populating the")
    print('\tdatabase files.db with the information in the /file/system filesystem tree.')
    print("")


def help_check():
    print(f"\n{command_name}  check  database_file  directory_to_check\n")
    print("database_file - required      - the path and filename of the files database to use")
    print("                                as a reference for possible duplicates.")
    print("directory_to_check - required - the directory to walk, to check against the file database")
    print("                                for potential duplicates.")
    print("\nExample:")
    print(f"\n{command_name} check /my/files.db /my/file/system\n")
    print("\tWill use the /my/files.db database file, and will tree walk through filesystem")
    print("\t/my/file/system and examine all files (from that path and lower). It will output")
    print("\tany potential duplicates found, where the total impact is greater than 1 MB (1000 KB)")
    print("")


def help_update():
    print(f"\n{command_name}  update  database_file  directory_to_check\n")
    print("database_file - required      - the path and filename of the files database to update")
    print("                                with the fileysstem info.")
    print("directory_to_check - required - the directory to walk, to gather info from to update the")
    print("                                file database to reflect.")
    print("\nExample:")
    print(f"\n{command_name} update /some/files.db /another/filesystem")
    print("\tWill use database file /some/files.db, will tree walk through the filesystem")
    print("\t/another/filesystem. The database will have new entries created for files not already")
    print('\tfound in the database, will have existing files updated, and will have missing files')
    print("\tremoved. When complete, the database information on the specified directly will")
    print("\texactly reflect the current contents and state of that directory.")
    print("")
