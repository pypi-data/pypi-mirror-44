import sqlite3

class db:
	def __init__(self, dbname):
		self.conn = sqlite3.connect(dbname, check_same_thread=False)

	def read(self, command, flat=True):
		cur = self.conn.cursor()
		cur.execute(command)
		f = cur.fetchall()
		if not f or not flat:
			return f
		else:
			if len(f[0]) == 1:
				f = [i[0] for i in f]
				if len(f) == 1:
					f = f[0]
			return f

	def read1(self, command):
		cur = self.conn.cursor()
		cur.execute(command)
		f = cur.fetchone()
		if len(f) == 1:
			f = f[0]
		return f
	
	def write(self, command):
		cur = self.conn.cursor()
		cur.execute(command)
		self.conn.commit()

	def __del__(self):
		self.conn.close()

