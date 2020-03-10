import xmltodict
import mysql.connector
import pprint
import json
import xml.etree.ElementTree as ElementTree
import os
from itunesLibrary import library
from mysql.connector import Error
from datetime import datetime

connection = None
class Track:
	def __init__(self, name, artist, alb_artist, comp, album, genre,kind,size,total_time, track_num, track_count, year, date_add, play_count, play_date, rel_date):

		self.name = name
		self.artist = artist
		self.alb_artist= alb_artist
		self.comp = comp
		self.album =album
		self.genre = genre
		self.kind = kind
		self.size = size
		self.total_time = total_time
		self.track_num = track_num
		self.track_count = track_count
		self.year = year
		self.date_add = XMLDateToSQL(date_add,datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
		self.play_count = play_count 
		self.play_date = XMLDateToSQL(play_date,self.date_add)
		self.rel_date = XMLDateToSQL(rel_date,self.date_add)


	def TrackToDB(self):
		connection = mysql.connector.connect(host='localhost',
									 database='MusicData',
									 user='eli',
									 password='Enzesws123',
									 auth_plugin='mysql_native_password')
	
		if(connection.is_connected()):
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("USE MusicData;")
			
		query = TrackInsertString(self)

		try:
			# print(query)
			cursor.execute(query)
		except mysql.connector.Error as err:
			print("SQL Error: {}".format(err))
		finally:
			connection.commit()
			connection.close()




class iTunesParser:
	'''Class for parsing an iTunes Library'''

	def __init__(self, input_file):
		'''Constructor'''
		self.source = input_file #Source file
		self.xml = ElementTree.parse(input_file) # Parsed XML File in a tree
		self.library = list() #List containing all the tracks


	def parse(self):
		'''Parse the file'''
		# Documentation about Element Tree ->  http://docs.python.org/2/library/xml.etree.elementtree.html
		root = self.xml.getroot()
		
		#Find index of element containing tracks
		i = 0
		
		for child in root[0]:
			if child.text == "Tracks":
				tracksIndex = i+1
				break
			i += 1
		
				
		#Loop trough all songs
		i = 0
		for song in root[0][tracksIndex]:
			#Every second element is a track
			if i % 2 == 1:
				
				#Loop through metadata of the track and extract info
				j = 0
				name = ""
				artist = ""
				alb_artist = ""
				comp = ""
				album = "" 
				genre = ""
				kind = ""
				size = 0
				total_time = 0 
				track_num = 0 
				track_count = 0 
				year = 0 
				date_add = 0
				play_count = 0
				play_date = 0
				rel_datet = 0



				for tag in song:
					if tag.text == "Name":
						name = song[j+1].text
					elif tag.text == "Artist":
						artist = song[j+1].text
					elif tag.text == "Album Artist":
						alb_artist = song[j+1].text
					elif tag.text == "Composer":
						comp = song[j+1].text
					elif tag.text == "Album":
						album = song[j+1].text
					elif tag.text == "Genre":
						genre = song[j+1].text
					elif tag.text == "Kind":
						kind = song[j+1].text
					elif tag.text == "Size":
						size = song[j+1].text
					elif tag.text == "Total Time":
						total_time = song[j+1].text
					elif tag.text == "Track Number":
						track_num = song[j+1].text
					elif tag.text == "Track Count":
						track_count = song[j+1].text
					elif tag.text == "Year":
						year = song[j+1].text
					elif tag.text == "Date Added":
						date_add = song[j+1].text
					elif tag.text == "Play Count":
						play_count = song[j+1].text
					elif tag.text == "Play Date":
						play_date = song[j+1].text
					elif tag.text == "Release Date":
						rel_date = song[j+1].text
					
					j += 1
				
				
				track = Track(name, artist, alb_artist, comp, album, genre,kind,
					size,total_time, track_num, track_count, year, date_add, play_count, play_date, rel_date)
				self.library.append(track)

				# print("play",track.play_date)
				# print("add",track.date_add)
				# print("rel",track.rel_date)
			
			i += 1			
			
		
		return
	def LibToDB(self):
		connection = mysql.connector.connect(host='localhost',
									 database='MusicData',
									 user='eli',
									 password='Enzesws123',
									 auth_plugin='mysql_native_password')
	
		if(connection.is_connected()):
			db_Info = connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)
			cursor = connection.cursor()
			cursor.execute("USE MusicData;")
		else:
			print("Error connecting to database, process aborted.")
			return
		
		for track in self.library:
			query = TrackInsertString(track)
			try:
				cursor.execute(query)
			except mysql.connector.Error as err:
				print("SQL Error: {}".format(err))
		
		

		connection.commit()
		connection.close()
		



	def __str__(self):
		'''Returns string of iTunes Library with all albums'''
		
		string = ""
		
		for i in range ( len(self.library) ):
			
			string += str(i+1)+". "
			
			string += str(self.library[i])
			
			if i != len(self.library) - 1:
				string += "\n"
		
		return string





def TrackInsertString(track):

	query = "INSERT INTO library (name, artist, album, album_artist, comp, genre, kind, total_time, track_num, track_count, year, date_added, play_count, play_date, rel_date)"
	query += "  VALUES ('" + track.name.replace("'","''") + "', '" + track.artist.replace("'","''") + "', '" +  track.alb_artist.replace("'","''") + "', '" +  track.comp.replace("'","''") + "', '"
	query += track.album.replace("'","''") + "', '" +  track.genre.replace("'","''") + "', '" +  track.kind.replace("'","''") + "', " +  str(track.size) + ", " +  str(track.total_time) + ", "
	query += "" + str(track.track_num) + ", " +  str(track.year)+ ", '" +  str(track.date_add)+ "', " +  str(track.play_count)+ ", '" +  str(track.play_date)+ "', '" +  str(track.rel_date) + "')"
	query+= ""
	# query = "WHERE NOT EXISTS ("
	# query += "SELECT * FROM library WHERE name = '" + track.name + "' AND artist = '" + track.artist + "' AND album = '" + track.album + "');"
	
	return query

def DBConnect():
	
	connection = mysql.connector.connect(host='localhost',
									 database='MusicData',
									 user='eli',
									 password='Enzesws123',
									 auth_plugin='mysql_native_password')
	
	if(connection.is_connected()):
		db_Info = connection.get_server_info()
		print("Connected to MySQL Server version ", db_Info)
		cursor = connection.cursor()
		cursor.execute("USE MusicData;")
		cursor.close()
		


	return connection

def XMLDateToSQL(date,default):
	if (date == 0):
		return default#datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
	if("-" not in date):
		return default#datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
		# date = datetime.date(datetime.now())
		
	
	date = date.replace("T", " ")
	date = date.replace("Z", "")

	return date
	

def main():

	# parser = iTunesParser("Library.xml")
	# parser.parse()
	# count = 0
	# for item in parser.library:
	# 	print(item.play_count, ",",item.name)
	# 	count += 1

	# print("total:",count)
	# try:
		

	parser = iTunesParser("Library.xml")
	parser.parse()	
	parser.LibToDB()


	# parser.library[len(parser.library)-2].TrackToDB()
		# for item in parser.library:
		# 	item.TrackToDB(cursor)
		# 	print()
		# 	print()

	# except Error as e:
	# 	print("Error while connecting to MySQL", e)
	# 	return

	# finally:
	# 	if (connection.is_connected()):
	# 		cursor.close()
	# 		connection.close()
	# 	print("MySQL connection is closed")
main()





















