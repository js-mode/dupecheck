#!/usr/local/bin/python3

import os


from config import DOT_PRINT, DIR_PATH_SEPARATOR


def build_db(file_db, directory, entertain=False):
	count = 0
	file_db.cleanup()

	for dirName, subdirList, fileList in os.walk(directory):
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
			
			if entertain:
				if count % DOT_PRINT == 0:
					print('.', end='', flush=True)
	return count

	
def print_matches(file_db, min_size):
	print("\nPossible matches by file size:\n")
	
	result = file_db.find_dup_filesizes()	
	
	for match in result:
		if min_size:
			if match[4] < min_size:
				break
		print(f"\tmatches: {match[3]}  file size: {match[2]}  total size: {match[4]:,}")

		files = file_db.find_files_of_size(match[2])
		for file in files:
			print(f"\t|\t{file[0]}{DIR_PATH_SEPARATOR}{file[1]}")
		print("")


	print("\nPossible matches by file name:\n")
		
	result = file_db.find_dup_filenames()
	for match in result:
		if min_size:
			if match[3] < min_size:
				break
		print(f"\tmatches: {match[2]}  file name: {match[1]}")
		files = file_db.find_files_of_name(match[1])
		for file in files:
			print(f"\t|\t{file[0]}{DIR_PATH_SEPARATOR}{file[1]}")
		print("")
