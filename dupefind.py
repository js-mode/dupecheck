#!/usr/local/bin/python3

import os
import sys

from utils import db


# CONSTANTS
DOT_PRINT = 1000
DIR_PATH_SEPARATOR = '/'


def usage(command_name):
	print("\nYou must pass a first parameter, which points to the filesystem you want to examine")
	print("for potential duplicates files.\n\n")
	print(f"{command_name} [directory] [cutoff size]")
	print("\nArguments:")
	print("directory - required - the directory to walk down through and look for duplicate files.")
	print("cutoff size - optional - the total space of any potential duplicates that falls below")
	print("                         this threshold, in bytes, will not be displayed.")
	print("                         This number is in KB (base 10). i.e. 1 means 1,000 bytes.\n")
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
	
	file_db = db.FileDatabase("./filebase.db")

	rootDir = sys.argv[1]
	count = 0
	for dirName, subdirList, fileList in os.walk(rootDir):
		for fname in fileList:
			# skip the garbage Mac general one
			# note this does not address the metadata files - .<filename> will still be picked up
			if fname == ".DS_Store":
				continue
			
			#insert file into database
			fullFileName = f"{dirName}{DIR_PATH_SEPARATOR}{fname}"
			statinfo = os.stat(fullFileName)
			fileSize = statinfo.st_size
			
			file_db.insert(dirName, fname, fileSize)
			
			count += 1
			
			if count % DOT_PRINT == 0:
				print('.', end='', flush=True)
	
	print(f"\n{count} files inserted into the database\n")
	
	print("\nPossible matches by file size:\n")
	
	result = file_db.find_dup_filesizes()	
	
	for match in result:
		if cutoff:
			if match[4] < cutoff:
				break
		print(f"\tmatches: {match[3]}  file size: {match[2]}  total size: {match[4]:,}")

		files = file_db.find_files_of_size(match[2])
		for file in files:
			print(f"\t|\t{file[0]}{DIR_PATH_SEPARATOR}{file[1]}")
		print("")


	print("\nPossible matches by file name:\n")
		
	result = file_db.find_dup_filenames()
	for match in result:
		if cutoff:
			if match[3] < cutoff:
				break
		print(f"\tmatches: {match[2]}  file name: {match[1]}")
		files = file_db.find_files_of_name(match[1])
		for file in files:
			print(f"\t|\t{file[0]}{DIR_PATH_SEPARATOR}{file[1]}")
		print("")
		

main()
