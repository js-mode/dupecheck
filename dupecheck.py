#!/usr/local/bin/python3

import os
import sys

from utils import db

import utils.functions
from commands import create, check, update

COMMANDS = {
	'create': create,
	'check': check,
	'update': update
}

def resolve_command(cmd):
	try:
		return COMMANDS[cmd]
	except KeyError:
		return None

def usage(command_name):
	print(f"{command_name}  command  database_file  directory_to_check")
	print("\nArguments:")
	print("command						 - Tells the utility what operation to perform with regard")
	print("								 - to the database. See commands list below.")
	print("database_file - required      - the path and filename of the files database to use for")
	print("                                comparison against.")
	print("directory_to_check - required - the directory to walk, and perform the specified command against.")
	print("\nCommands:")
	print("create - Create the database (i.e. it does not already exist). If the database file does")
	print("			already exist, then the process will abort with an error. Otherwise, the database")
	print("			file will be created and processing will proceed as if an update command had given")
	print("			on an existing database file.")
	print("check  - Check the specified directory for duplicate entries in the file database, and")
	print("			display any potential matches for review.")
	print("update - Will modify the database entries for this directory to match the directory")
	print("			specified. NOTE that this will mean adding new files, updating stats on existing")
	print("			existing files, and removal of files in the database that are not in the filesystem.")
	print("\nExamples:")
	print(f"\n{command_name} create /files.db /file/system\n")
	print("\tWill create the database files.db (or will abort with an error if that database file")
	print("\talready exists). Then will perform like an update command, which means populating the")
	print('\tdatabase files.db with the information in the /file/system filesystem tree.')
	print(f"\n{command_name} check /my/files.db /my/file/system\n")
	print("\tWill use the /my/files.db database file, and will tree walk through filesystem")
	print("\t/my/file/system and examine all files (from that path and lower). It will output")
	print("\tany potential duplicates found, where the total impact is greater than 1 MB (1000 KB)")
	print("")
	print(f"\n{command_name} update /some/files.db /another/filesystem")
	print("\tWill use database file /some/files.db, will tree walk through the filesystem")
	print("\t/another/filesystem. The database will have new entries created for files not already")
	print('\tfound in the database, will have existing files updated, and will have missing files')
	print("\tremoved. When complete, the database information on the specified directly will")
	print("\texactly reflect the current contents and state of that directory.")
	return


def main():

	if len(sys.argv) < 4:
		usage(sys.argv[0])
		sys.exit(1)
	
	command = sys.argv[1]
	parameters = sys.argv[2:]

	command_handler = resolve_command(command)
	if command_handler is None:
		print(f"\nInvalid command: '{command}'\n")
		usage(sys.argv[0])
		sys.exit(2)
	
	command_handler(parameters)

	sys.exit(0)

	file_db = db.FileDatabase(db_filename)
	tot_matches = 0
	tot_adds = 0
	tot_skips = 0
	
	for dirName, subdirList, fileList in os.walk(dir_to_walk):
		for fname in fileList:
			# skip the garbage Mac general one
			# note this does not address the metadata files - .<filename> will still be picked up
			if fname == ".DS_Store":
				continue
			
			#insert file into database
			fullFileName = f"{dirName}{DIR_PATH_SEPARATOR}{fname}"
			statinfo = os.stat(fullFileName)
			file_size = statinfo.st_size
			
			if option == "add":
				in_database = file_db.find_specific_file(dirName, fname)
				if len(in_database) > 0:
					print(f"Skipping {dirName}{DIR_PATH_SEPARATOR}{fname} already in database {db_filename}")
					tot_skips += 1
				else:
					file_db.insert(dirName, fname, file_size)
					print(f"ADDED {dirName}{DIR_PATH_SEPARATOR}{fname} into in database {db_filename}")
					tot_adds += 1
				continue
			
			matches = file_db.find_files_of_size(file_size)
			if len(matches) > 0:
				found = 0
				for match in matches:
					if dirName == match[0] and fname == match[1]:
						continue
					found += 1
					if found == 1:
						print(f"Potential SIZE matches for {fullFileName}:")
					print(f"| \t{match[0]}{DIR_PATH_SEPARATOR}{match[1]}")
				if found:
					print("")
					tot_matches += 1
				
			matches = file_db.find_files_of_name(fname)
			if len(matches) > 0:
				found = 0
				for match in matches:
					if dirName == match[0] and fname == match[1]:
						continue
					found += 1
					if found == 1:
						print(f"Potential NAME matches for {fullFileName}:")
					print(f"| \t{match[0]}{DIR_PATH_SEPARATOR}{match[1]}")
				if found:
					print("")
					tot_matches += 1

	if tot_matches == 0 and option != "add":
		print("\nNo duplicates found.\n")
	elif option == "add" and tot_adds == 0:
		print(f"\nNo files added to database {db_filename}  Skipped: {tot_skips}\n")
	elif option == "add":
		print(f"\nAdded {tot_adds} files to database {db_filename}  Skipped: {tot_skips}\n")
				

main()
