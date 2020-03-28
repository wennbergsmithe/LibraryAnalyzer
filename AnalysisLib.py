# AnalyisiLib.py
# Written by Elijah Wennberg-Smith
# Last Edited: 3.26.20

from Track import Track
from ItunesParser import iTunesParser
from SQLConnector import DBConnector
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from os import path
from globals import db
import altair as alt
import pandas as pd

# Updates database from a pre-exported file in the lib_backups directory. 
# Itunes no longer automatically update the xml file, so it must be exported manually through itunes app. 
# command: u <file name>/<"a">
#	- a adds all files in lib_backups in order given they are labeled 1.xml, 2.xml, ..., n.xml

def updateDBFromXML(arg):
	if(arg != "a"):
		fp = "lib_backups/" + arg
		print(fp)
		if(not path.exists(fp)):
			print("invalid xml file. Make sure to include file extension")
			return
		
		parser = iTunesParser(fp)

		print("Parsing XML file...")
		parser.parse()
		print("Parsing complete, exporting library to database...")
		parser.LibToDB()
	else:
		i = 1
		more = True
		while(more):
			fp = "lib_backups/" + str(i) + ".xml"
			print(fp)
			if(path.exists(fp)):
				parser = iTunesParser(fp)
				print("Parsing " + fp)
				parser.parse()
				print("Parsing complete, exporting library to database...")
				parser.LibToDB()
			else:
				more = False
			i += 1
		        
def GenreStreamGraph():
	#incomplete

	db.query("SELECT DISTINCT(YEAR(date_added)) yr FROM library ORDER BY yr;")
	years = []
	for r in db.rs:
		years.append(r['yr'])
	db.query("SELECT DISTINCT(genre) g FROM library ORDER BY g;")
	genres = []

	x = []
	x.append("year")
	for r in db.rs:
		genres.append(r['g'])
		x.append(r['g'])
	y = []
	for yr in years:
		ty = []
		ty.append(yr)
		i = 0
		for g in genres:
			db.query("SELECT COUNT(id) AS c FROM library WHERE YEAR(date_added) = " + str(yr) + " AND genre = '" + g + "';")
			for r in db.rs:
				ty.append(r['c'])
		y.append(ty)


	# print(x)
	df = pd.DataFrame([y], index=x)
	print(df)

# overall library growth over time
# command: lg
def LibGrowthChart():
	print("Gathering data... ")
	y = []
	x = []
	i = 0
	db.query("SELECT DATE(date_added) AS d FROM library ORDER BY d ASC;")

	for date in db.rs:
		i+=1
		x.append(date['d'])
		y.append(i)

	print("Be sure to close chart window before continuing.")
	plt.plot(x,y)
	plt.gcf().autofmt_xdate() 
	plt.show()

#chart of overall listening history
#command: lc
def listenChart():
	y = []
	x = []
	print("Gathering data...")
	global db 
	db.query("SELECT COUNT(record_id) AS count, DATE(listen_date) AS date FROM listening_history GROUP BY date ORDER BY date;")

	for date in db.rs:
		x.append(date['date'])
		y.append(date['count'])

	print("Be sure to close chart window before continuing.")
	plt.plot(x,y)
	plt.gcf().autofmt_xdate() 
	plt.show()

# Top artists by number of songs from them. 
# optional x argument specifies how long the list is, default is 10
# command: tas <optional leng>
def TopXArtistsBySongs(leng=10):
	db.query("SELECT COUNT(id) AS cnt, artist FROM library GROUP BY artist ORDER BY cnt DESC LIMIT " + str(leng) + ";")
	ret = db.rs

	i = 0
	for song in ret:
		i += 1
		print("#" + str(i) + " ==============================")
		print("Artist: " + song["artist"])
		print("Number Of Songs: " + str(song["cnt"]))
		print()
		


def SongSkipProbability(x, asc=1, zeros_ones=0):
	# This function calculates the probability of skipping each song and displays in a list of x length.
	# Also displays the ratio of skips to plays
	# Set asc=1 to list in ascending order, asc=0 for descending.
	# Set zeros_ones=1 to include arists with values of 0 or 1. In large datasets there can be an overwheling number of both.
	# command: sprob <x = length> < asc = boolean for ascending or descending> <zeros_ones = boolean to include probs of 0 or 1>
	if asc:
		ordr = "ASC"
	else:
		ordr = "DESC"

	db.query("SELECT skip_count/(skip_count+play_count) AS p, name, artist, skip_count as skips, play_count as listens FROM library ORDER BY p " + ordr +";")
	ret = db.rs
	i = 0
	for song in ret:
		if(song["p"] != None):#and
			if(zeros_ones or (song["p"] > 0.000000 and song["p"] < 1.0)):
				i += 1
				print("#" + str(i) + " ==============================")
				print("Song: " + song["name"])
				print("Artist: " + song["artist"])
				print("Probability of skipping: " + str(song["p"]))
				print("Ratio of skips to plays: " + str(song["skips"]) + ":" + str(song["listens"]) )
				print()
				if(i==x):
					break

def GenreSkipProbability(x, asc=1, zeros_ones=0):
	# This function calculates the probability of skipping each genre and displays in a list of x length.
	# Also displays the ratio of skips to plays
	# Set asc=1 to list in ascending order, asc=0 for descending.
	# Set zeros_ones=1 to include arists with values of 0 or 1. In large datasets there can be an overwheling number of both.
	# command: gprob <x = length> < asc = boolean for ascending or descending> <zeros_ones = boolean to include probs of 0 or 1>
	
	if asc:
		ordr = "ASC"
	else:
		ordr = "DESC"

	db.query("SELECT SUM(skip_count)/(SUM(skip_count)+SUM(play_count)) AS p, genre, SUM(skip_count) as skips, SUM(play_count) as listens FROM library GROUP BY genre ORDER BY p " + ordr +";")
	ret = db.rs
	i = 0
	for song in ret:
		if(song["p"] != None):#and
			if(zeros_ones or (song["p"] > 0.000000 and song["p"] < 1.0)):
				i += 1
				print("#" + str(i) + " ==============================")
				print("Genre: " + song["genre"])
				print("Probability of skipping: " + str(song["p"]))
				print("Ratio of skips to plays: " + str(song["skips"]) + ":" + str(song["listens"]) )
				print()
				if(i==x):
					break

def ArtistSkipProbability(x, asc=1, zeros_ones=0):
	# This function calculates the probability of skipping each artist and displays in a list of x length.
	# Also displays the ratio of skips to plays
	# Set asc=1 to list in ascending order, asc=0 for descending.
	# Set zeros_ones=1 to include arists with values of 0 or 1. In large datasets there can be an overwheling number of both.
	# command: aprob <x = length> < asc = boolean for ascending or descending> <zeros_ones = boolean to include probs of 0 or 1>
	
	if asc:
		ordr = "ASC"
	else:
		ordr = "DESC"

	db.query("SELECT SUM(skip_count)/(SUM(skip_count)+SUM(play_count)) AS p, artist, SUM(skip_count) as skips, SUM(play_count) as listens FROM library GROUP BY artist ORDER BY p " + ordr +";")
	ret = db.rs
	i = 0
	for song in ret:
		if(song["p"] != None):#and
			if(zeros_ones or (song["p"] > 0.000000 and song["p"] < 1.0)):
				i += 1
				print("#" + str(i) + " ==============================")
				print("Artist: " + song["artist"])
				print("Probability of skipping: " + str(song["p"]))
				print("Ratio of skips to plays: " + str(song["skips"]) + ":" + str(song["listens"]) )
				print()
				if(i==x):
					break


def NumSongsByYear(x=10):
	# prints top x years based on number of songs
	# command sby <x = length>
	db.query("SELECT COUNT(id) AS sm, year FROM library GROUP BY year ORDER BY sm DESC LIMIT " + str(x) + ";")
	ret = db.rs


	i = 0
	for song in ret:
		i += 1
		print("#" + str(i) + " ==============================")
		print("Year: " + str(song["year"]))
		print("Number of Songs: " + str(song["sm"]))
		print()

def MonthsBySongsAdded():
	# produces a chart of total songs added for each month of the year
	# command: monchart

	db.query("SELECT count(id) AS cnt, MONTH(date_added) AS month FROM library GROUP BY MONTH(date_added) ORDER BY month ASC ;")
	ret = db.rs
	x = []
	y = []
	i = 0
	for song in ret:
		x.append(song['month'])
		y.append(song['cnt'])
		
	fig, ax = plt.subplots()
	plt.bar(x, y)
	plt.xticks(x, ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec',))
	plt.show()

def TopXGenresBySongs(x=10):
	#top x genres by the number of songs in that genre
	# command: gbs <x - optional list len>
	db.query("SELECT COUNT(id) AS cnt, genre FROM library GROUP BY genre ORDER BY cnt DESC LIMIT " + str(x) + ";")
	ret = db.rs

	i = 0
	for song in ret:
		i += 1
		print("#" + str(i) + " ==============================")
		print("Genre: " + song["genre"])
		print("Number Of Songs: " + str(song["cnt"]))
		print()

def TopXSongsByPlays(x=10):
	# top x songs by play count
	# command sbp <optional x list len>
	if(x<1):
		return

	db.query("SELECT * FROM library ORDER BY play_count DESC LIMIT " + str(x) + ";")
	ret = db.rs

	i = 0
	for song in ret:
		i += 1
		print("#" + str(i) + " ==============================")
		print("Title: " + song["name"])
		print("Artist: " + song["artist"])
		print("Play Count: " + str(song['play_count']))
		print()
# db.execute("USE musicdata")
# GenreStreamGraph()
# db.disconnect()


