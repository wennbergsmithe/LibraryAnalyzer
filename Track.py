# Track.py
# Written by Elijah Wennberg-Smith 
# Last Edited: 3.26.20
#
# Track UDT used for storing track data at runtime

from SQLConnector import DBConnector
from datetime import datetime

class Track:
	def __init__(self, name, artist, album, alb_artist, comp, genre, kind,size,total_time, track_num, 
				 track_count, year, date_add, play_count, play_date, rel_date, skip_count):

		self.name = name
		self.artist = artist
		self.alb_artist= alb_artist
		self.comp = comp
		self.album = album
		self.genre = genre
		self.kind = kind
		self.size = size
		self.total_time = total_time
		self.track_num = int(track_num)
		self.track_count =int(track_count)
		self.year = int(year)
		self.date_add = XMLDateToSQL(date_add,datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
		self.play_count = int(play_count)
		self.play_date = XMLDateToSQL(play_date,self.date_add)
		self.rel_date = XMLDateToSQL(rel_date,self.date_add)
		self.skip_count = int(skip_count)

		

def XMLDateToSQL(date,default):
	if ((date == 0) or (date == None) or ("-" not in date)):
		return default

	date = date.replace("T", " ")
	date = date.replace("Z", "")


	

	return date


