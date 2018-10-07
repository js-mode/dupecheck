#!/usr/local/bin/python3

import os


def is_file(filename):
    """
    Checks to see if the filename passed in is a file or not
    :param filename: filename to check
    :return: True if it is a file, otherwise false
    """
    return os.path.isfile(filename)


def is_dir(dirname):
    """
    Checks to see if the directory name/path passed in is a directory or not
    :param dirname: directory name/path to check
    :return: True if it is a file, otherwise false
    """
    return os.path.isdir(dirname)


def normalize_dir_name(dirname):
	"""
	Function to normalize a directory name. Make sure there is no trailing os separator, and
	convert it to an absolute path
	:param dirname: the directory name to normalize
	:return: the normalized directory name - full absolute path, with no trailing OS separator
	"""
	temp = dirname.rstrip(os.sep)
	return os.path.abspath(temp)


def treewalk_with_action(file_db, directory, filter, worker, in_state = None):
	"""
	Perform a treewalk on a specified filesystem, including all subdirectories and files. Will skip
	any file namess in the filter list, and will execute the worker function, passing it a dictionary
	to maintain state.
	NOTE: If state['STOP'] exists, then the treewalk will immediately halt.
	:param file_db: the FileDatabase class object that connects to a file database file
	:    directory: a string specifying the filesystem tree to walk through
	:       filter: a list of specific filename strings (not reg exp or wildcards) to skip over
	;             : in the treewalk (e.g. '.DS_Store" for Mac native, etc.)
	:       worker: a helper worker function to be executed on each file found.
	:             : worker signature;  worker(file_db, directory, filename, filesize, state_dict)
	:     in_state: Optional parameter. Allows a pre-populated state dictionary to come in, to be
	;             : used by the helper (i.e. pass flags, settings, etc. specific to this run)
	;return: a final state dictionary. the calling handler is expected to know how to access and
	:      : interpret the data in it, as it is being populated by the worker function passed in.
	"""
	if not in_state:
		state = dict()
	else:
		state = in_state

	for dirName, subdirList, fileList in os.walk(directory):
		for fname in fileList:
			# immediately halt if we get the STOP flag
			if 'STOP' in state:
				return state

			# skip any filtered filename (exact) matches
			# e.g. .DS_Store
			if fname in filter:
				continue
			
			#get file size
			fullFileName = os.path.join(dirName, fname)
			statinfo = os.stat(fullFileName)
			fileSize = statinfo.st_size
			
			worker(file_db, dirName, fname, fileSize, state)
	return state


# leaving this in for future reporting command	
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
			print(f"\t|\t{file[0]}{os.sep}{file[1]}")
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
			print(f"\t|\t{file[0]}{os.sep}{file[1]}")
		print("")
