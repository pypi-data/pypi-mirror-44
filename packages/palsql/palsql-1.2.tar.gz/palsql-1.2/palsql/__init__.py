import sqlite3

class db:
	def __init__(self, dbname):
		self.conn = sqlite3.connect(dbname)

	def read(self, command, flat=True):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute(command)
				f = self.cur.fetchall()
				if not f or not flat:
					return f
				else:
					if len(f[0]) == 1:
						f = [i[0] for i in f]
						if len(f) == 1:
							f = f[0]
					return f

	def read1(self, command):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute(command)
				f = self.cur.fetchone()
				if len(f) == 1:
					f = f[0]
				return f
	
	def write(self, command):
		with self.conn:
			with self.conn.cursor() as cur:
				cur.execute(command)
				cur.commit()

	def __del__(self):
		self.conn.close()

