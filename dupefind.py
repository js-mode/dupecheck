#!/usr/local/bin/python3

import sys

from utils import db

import utils.functions


# CONSTANTS
from config import DB_FILE


def usage(command_name):
	print(f"\n{command_name} directory [cutoff size]")
	print("\nArguments:")
	print("directory - required - the directory to walk down through and look for duplicate files.")
	print("cutoff size - optional - the total space of any potential duplicates that falls below")
	print("                         this threshold, in KB (kilobytes), will not be displayed.")
	print("                         This number is in base 10. i.e. 1 means 1,000 bytes.\n")
	print("Examples:\n")
	print(f"{command_name} /my/file/system\n")
	print("\tWill tree walk through filesystem /my/file/system and examine all files")
	print("\tfrom that path and lower.\n")
	print(f"{command_name} /another/filesystem 100000\n")
	print("\tWill stop returning results once the total space occupied by the potential")
	print("\tduplicates falls below ~100 KB (base 10).\n")
	return


def main():

	if len(sys.argv) == 1:
		usage(sys.argv[0])
		sys.exit(1)
		
	if len(sys.argv) >= 3:
		try:
			cutoff = int(sys.argv[2])
			cutoff *= 1000
		except ValueError as err:
			print("\n\nError, cutoff argument must be an integer.")
			print("Value passed as second argument: '{sys.argv[2]}'\n\n")
			return
	else:
		cutoff = None
	
	file_db = db.FileDatabase(DB_FILE)
	rootDir = sys.argv[1]
	
	count = utils.functions.build_db(file_db, rootDir, entertain=True)	
	print(f"\n{count} files inserted into the database\n")
	
	utils.functions.print_matches(file_db, cutoff)
	

main()
