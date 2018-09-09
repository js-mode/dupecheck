#!/usr/local/bin/python3

import os
import sys

from utils import db

import utils.functions


# CONSTANTS
from config import DIR_PATH_SEPARATOR


def usage(command_name):
	print("\nRequired arguments missing.\n")
	print(f"{command_name} database_file directory_to_check [add]")
	print("\nArguments:")
	print("database_file - required      - the path and filename of the files database to use for")
	print("                                comparison against.")
	print("directory_to_check - required - the directory to walk, and compare files for possible")
	print("                                duplicate matches in the database.")
	print("add - optional                - string literal 'add'. If supplied, the files found in")
	print("                                the directory will have their info added to the")
	print("                                specified database file.")
	print("Examples:\n")
	print(f"{command_name} /my/files.db /my/file/system\n")
	print("\tWill use the /my/files.db database file, and will tree walk through filesystem")
	print("\t/my/file/system and examine all files (from that path and lower)")
	print("")
	print(f"{command_name} /some/files.db /another/filesystem add")
	print("\tWill use database file /some/files.db, will tree walk through the filesystem")
	print("\t/another/filesystem, and will add the files it finds into the database /some/files.db")
	print("\tIt will not perform file match checking, as you have specified it to add the files.")
	print("\n\tThe add option would typically be done after a first run without that option, and")
	print("\tany duplicates eliminated. Then a second run with add will update the database with")
	print("\tthe new info, for future comparison runs.\n")
	return


def main():

	if len(sys.argv) < 3:
		usage(sys.argv[0])
		sys.exit(1)
	
	db_filename = sys.argv[1]
	dir_to_walk = sys.argv[2]
		
	if len(sys.argv) >= 4:
		option = sys.argv[3].lower()
		if option != "add":
			print(f"\nUnsupported option: {option}\n")
			usage(sys.argv[0])
			sys.exit(2)
	else:
		option = None
	
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
