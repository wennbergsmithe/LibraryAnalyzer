# SQLConnector.py
# Written by Elijah Wennberg-Smith 
# Last Edited: 3.26.20
#
# This class is a wrapper for the mysql connector class, tailored for Library Analyzer. 

import mysql.connector
from mysql.connector import Error

class DBConnector():


	def __init__(self):
		#establishes connection to the music data database
		self.connection = mysql.connector.connect(host='localhost',
									 user='eli',
									 password='pass', #secure
									 auth_plugin='mysql_native_password')
	
		if(self.connection.is_connected()):
			self.db_Info = self.connection.get_server_info()
			self.cursor = self.connection.cursor()
			self.rs = []
			print("Connected to MySQL Server version ", self.db_Info)
		else:
			print("failed to establish database connection")
			raise ValueError

	def execute(self,statement):
		try:
			# print(query)
			self.cursor.execute(statement)
		except mysql.connector.Error as err:
			print("SQL Error: {}".format(err))
			print("\t"+statement)
			return -1
		finally:
			self.connection.commit()

	def changeDB(self, dbName):
		self.execute("USE "+ dbName + ";")

	def query(self,query):
		try:
			# print(query)
			self.cursor.execute(query)
			desc = self.cursor.description
			column_names = [col[0] for col in desc]
			self.rs = [dict(zip(column_names, row)) for row in self.cursor.fetchall()]

		except mysql.connector.Error as err:
			print("SQL Error: {}".format(err))
			print("\t"+query)
			return -1


	def executeFile(self, filename):
		fd = open(filename, 'r')
		sqlFile = fd.read()
		fd.close()
		sqlCommands = sqlFile.split(';')
		for command in sqlCommands:
			self.execute(command)
	
	def newDB(self, db_name):
		if(self.execute("CREATE DATABASE " + db_name) != -1):
			self.execute("USE " + db_name)
			self.executeFile("SQL/library.sql")
		else:
			print("Database not created.")
			return -1

	def getDB(self):
		self.query("SELECT DATABASE();")
		return self.rs[0]['DATABASE()']



	def disconnect(self):
		self.cursor.close()
		self.connection.close()
		print("Closed connection to " + self.db_Info)
