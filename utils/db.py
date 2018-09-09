import sqlite3


connection = None


class FileDatabase:
	
	def __init__(self, filename):
		self.connection = sqlite3.connect(filename)
		self.cursor = self.connection.cursor()
		self.cleanup()
		
	def cleanup(self):
		self.cursor.execute('''DROP TABLE IF EXISTS files''')
		self.cursor.execute('''DROP INDEX IF EXISTS filename''')
		self.cursor.execute('''DROP INDEX IF EXISTS filesize''')
		self.build_db()
		
	def build_db(self):
		self.cursor.execute('''CREATE TABLE files (filedir, filename, filesize) ''')
		self.cursor.execute('''CREATE INDEX filename on files(filename)''')
		self.cursor.execute('''CREATE INDEX filesize on files(filesize)''')
	
	def insert(self, filedir, filename, filesize):
		#vals = f"('{filename}', {filesize})"
		vals = (f"{filedir}", f"{filename}", filesize)
		self.cursor.execute('''INSERT INTO files VALUES (?, ?, ?)''', vals)
		
	def find_dup_filesizes(self):
		self.cursor.execute('''SELECT filedir, filename, filesize, count(*), sum(filesize) AS totsize FROM files GROUP BY filesize having count(*) > 1 ORDER BY totsize DESC''')
		return self.cursor.fetchall()
		
	def find_files_of_size(self, size):
		val = (size,)
		self.cursor.execute('''SELECT filedir, filename FROM files WHERE filesize=?''', val)
		return self.cursor.fetchall()
		
	def find_dup_filenames(self):
		self.cursor.execute('''SELECT filedir, filename, count(*), sum(filesize) AS totsize FROM files GROUP BY filename having count(*) > 1 ORDER BY totsize DESC''')
		return self.cursor.fetchall()
		
	def find_files_of_name(self, name):
		val = (name,)
		self.cursor.execute('''SELECT filedir, filename, sum(filesize) AS totsize FROM files WHERE filename=?''', val)
		return self.cursor.fetchall()
		
		