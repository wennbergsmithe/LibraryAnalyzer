# AnalyisiLib.py
# Written by Elijah Wennberg-Smith
# Last Edited: 3.26.20

from ItunesParser import iTunesParser
from SQLConnector import DBConnector
import re

def PlayListUnheard(x=50, genre="recent", since=1900):
	# generates a playlist of songs that have not been heard before. 
	# pass x for list len, genre to specify genre(x most recent are used as default), and min year released for playlist.
	# prints artist and song
	dbc = DBConnector()
	db2 = DBConnector()
	i = 0
	if(genre.lower() == "rap"): genre += " hip hop "

	if(genre == "recent"):
		
		q = "SELECT genre FROM library ORDER BY play_date DESC LIMIT " + str(x) + ";" 
		

		dbc.query(q)
				
		for row in dbc.rs:
			gen = row["genre"]

			q2 = "SELECT SUBSTRING(name,1,50) as name, SUBSTRING(artist,1,50) as artist FROM library WHERE genre LIKE '" + gen + "' AND play_count = 0 AND YEAR(rel_date) >= " + str(since) + " ORDER BY RAND() LIMIT 1;"
			db2.query(q2)
			for row2 in db2.rs:
				i += 1
				name = row2["name"]
				artist = row2["artist"]

				print("#" + str(i) + " ===========================")
				print("\tSong: " + name)
				print("\tArtist: " + artist)
			
	else:
		words = re.findall(r"[\w']+", genre)
		genrestr = ""
		for word in words:
			genrestr += " genre LIKE '%" + word + "%' OR"
		genrestr = genrestr[:-3]

		q2 = "SELECT SUBSTRING(name,1,50) as name, SUBSTRING(artist,1,50) as artist, genre FROM library WHERE " + genrestr + " AND play_count = 0 AND YEAR(rel_date) >= " + str(since) + " ORDER BY RAND() LIMIT " + str(x) + ";"
		db2.query(q2)

		for row2 in db2.rs:
			i += 1
			name = row2["name"]
			artist = row2["artist"]
			genre = row2["genre"]

			print("#" + str(i) + " ===========================")
			print("\tSong: " + name)
			print("\tArtist: " + artist)
			print("\tGenre:" + genre)


	dbc.disconnect()
	db2.disconnect()

















