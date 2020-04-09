# ItunesParser.py
# Written by Elijah Wennberg-Smith 
# Last Edited: 3.26.20
#
# This class parses the Apple Music XML file, groups songs into Track objects,
# then pushes library changes to the database.

import xml.etree.ElementTree as ElementTree
from Track import Track
from SQLConnector import DBConnector
import progressbar
import re
from globals import db
import squarify
import matplotlib.pyplot as plt

class iTunesParser:
	#parses xml file from iTunes 

	def __init__(self, file):

		self.source = file #Source file
		self.xml = ElementTree.parse(file) # Parsed XML File
		self.library = list() #List containing all the tracks


	def parse(self):
		# parse the xml file
		root = self.xml.getroot()
		
		#Find index of element containing tracks
		i = 0
		
		for sub in root[0]:
			if sub.text == "Tracks":
				trIndex = i+1
				break
			i += 1
		
				
		#Loop trough all songs
		i = 0
		for song in root[0][trIndex]:
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
				rel_date = 0
				skip_count = 0
				create = True



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
						# agrigate viariations of same genre
						genre = song[j+1].text
						if(genre == "Hip Hop/Rap" or genre == "Hip-Hop" or genre == "Hip Hop" or genre == "Rap"):
							genre = "Hip-Hop/Rap"
						elif(genre == "Africa"):
							genre = "African"
						elif(genre == "Blues-Rock" or genre == "Blues Rock"):
							genre = "Blues/Rock"
						elif(genre == "Popular"):
							genre = "Pop"
						elif(genre == "R&B Soul"):
							genre = "R&B/Soul"
						elif(genre == "Classic Rock" or genre == "Rock & Roll" or genre == "Rock/Pop" or genre == "General Rock"):
							genre = "Rock"
						elif (genre == "Audiobook" or genre == "Podcast"): # ignore audiobooks and podcasts
							create = False
						elif(genre == " " or genre == ""):
							genre = "No Genre"

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
					elif tag.text == "Play Date UTC":
						play_date = song[j+1].text
					elif tag.text == "Release Date":
						rel_date = song[j+1].text
					elif tag.text == "Skip Count":
						skip_count = song[j+1].text
					j += 1
				
				if(create):
					track = Track(name, artist, album, alb_artist, comp, genre,kind,size,total_time, track_num, track_count, year, date_add, play_count, play_date, rel_date,skip_count)
					self.library.append(track)
			i += 1
		return

	def LibToDB(self):

		bar = progressbar.ProgressBar(maxval=len(self.library),widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		bar.start()
		i = 0
		for track in self.library:
			i+=1
			bar.update(i)
			stmt = "SELECT id, play_count, skip_count "						# first check if the song exists in
			stmt += " FROM library "										# the library already. 
			stmt += "WHERE name = '" + track.name.replace("'","''")
			stmt += "' AND artist = '" + track.artist.replace("'","''") 
			stmt += "' AND album = '" + track.album.replace("'","''") 
			stmt += "' AND track_num = " + str(track.track_num) + ";"
			db.query(stmt)

			if(db.rs == []):												# if the record does not exist,
				stmt = " INSERT INTO library "								# insert it into the library table
				stmt += "             (name, artist, album, album_artist, "
				stmt += "             comp, genre, kind, total_time, track_num,"
				stmt += "             track_count, year, date_added, play_count, "
				stmt += "             play_date, rel_date, skip_count)"
				stmt += "      VALUES ('" + track.name.replace("'","''") + "', '" + track.artist.replace("'","''") + "', '" + track.album.replace("'","''") + "', '" +  track.alb_artist.replace("'","''") + "', '"
				stmt +=  track.comp.replace("'","''") + "', '" +  track.genre.replace("'","''") + "', '" +  track.kind.replace("'","''") + "', " +  str(track.total_time) + ", "
				stmt += str(track.track_num) + ", " + str(track.track_count) + ", " + str(track.year)+ ", DATE_ADD('" +  str(track.date_add)+ "', INTERVAL -4 DAY), "
				stmt += str(track.play_count)+ ", DATE_ADD('" +  str(track.play_date)+ "', INTERVAL -4 DAY), DATE_ADD('" +  str(track.rel_date) + "', INTERVAL -4 DAY), " + str(track.skip_count) + ");"
				db.execute(stmt)
				last_id = db.cursor.lastrowid

				if(track.play_count > 0):											# if there are plays, insert last play into listening history
					
					if(int(track.play_date[:4]) > 2000):
						stmt = "INSERT INTO listening_history (track_id, listen_date, listen_count)"
						stmt += "    VALUES (" + str(last_id) + ","
						stmt += "           DATE_ADD('" + str(track.play_date) + "', INTERVAL -4 DAY),"
						stmt += "            1);"
						db.execute(stmt)

			else:											# if the record does exist

				track_id = db.rs[0]['id']					# track id
				db_pc = db.rs[0]['play_count']				# current listen count
				if(db_pc == None):
					db_pc = 0
				db_sc = db.rs[0]['skip_count']				# current skip count
				if(db_sc == None):
					db_sc = 0


				
				if (track.play_count > db_pc or track.skip_count > db_sc):	# if there are new plays or skips
									
					if (track.play_count > db_pc ):							# for new plays only:
						q = "SELECT record_id FROM listening_history WHERE track_id = " + str(track_id) + " AND listen_date = '" + str(track.play_date) + "';"
						db.query(q)
						if(db.rs == []):									# new listen record in listening history
							stmt = "INSERT INTO listening_history (track_id, listen_date, listen_count)"
							stmt += "    VALUES (" + str(track_id) + ","
							stmt += "           DATE_ADD('" + str(track.play_date) + "', INTERVAL -4 DAY),"
							stmt += "            1);"
							db.execute(stmt)
																			# for new plays and new skips:
					stmt = "UPDATE library "								# update data in library
					stmt += "  SET play_count = " + str(track.play_count) + ", "
					stmt += "      total_time = " + str(track.total_time) + ", "
					stmt += "      play_date = DATE_ADD('" + str(track.play_date) + "', INTERVAL -4 DAY), "
					stmt += "      skip_count = " + str(track.skip_count) + " "
					stmt += "WHERE id = " + str(track_id) + ";"
					db.execute(stmt)
					
		bar.finish()













