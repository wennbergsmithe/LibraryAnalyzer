# AnalyisiLib.py
# Written by Elijah Wennberg-Smith
# Last Edited: 3.26.20

from ItunesParser import iTunesParser
import matplotlib
import matplotlib.pyplot as plt
import squarify
from globals import db
import altair as alt
import pandas as pd
import webbrowser
import os

# Updates database from a pre-exported file in the lib_backups directory. 
# Itunes no longer automatically update the xml file, so it must be exported manually through itunes app. 
# command: u <file name>/<"a">
#	- a adds all files in lib_backups in order given they are labeled 1.xml, 2.xml, ..., n.xml

def updateDBFromXML(arg):
	if(arg != "a"):
		fp = "lib_backups/" + arg
		print(fp)
		if(not os.path.exists(fp)):
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
			if(os.path.exists(fp)):
				parser = iTunesParser(fp)
				print("Parsing " + fp)
				parser.parse()
				print("Parsing complete, exporting library to database...")
				parser.LibToDB()
			else:
				more = False
			i += 1

def GenreStreamGraphPlays():
	genres = []
	years = []
	counts = []
	db.query("SELECT COUNT(id) count, genre FROM library GROUP BY genre ORDER BY count DESC LIMIT 27;")
	
	for genre in db.rs:
 		genres.append(genre['genre'])

	data = []
	db.query("SELECT DISTINCT YEAR(listen_date) year FROM listening_history  ORDER BY year;")
	years = [item['year'] for item in db.rs]
	print("Gathering data... This might take a bit")
	for year in years:
		for month in range(1,13):
			for genre in genres:
				db.query("SELECT count(record_id) count FROM listening_history LEFT JOIN library ON track_id = id WHERE genre = '" + genre + "' AND MONTH(listen_date) = " + str(month) + " AND YEAR(listen_date) = " + str(year)+ ";")
				for item in db.rs:

					if(month<10):
						s_month = "0" + str(month)
					else:
						s_month = str(month)
					date = str(year) + "-" + s_month# + "-01T01:00:00.000Z"
					# print(date)
					temp = {"date": date, "genre":genre, "count": item['count']}
					data.append(temp)
# , scale=alt.Scale(domain=(0,1000))

	df = pd.DataFrame(data=data)
	streamgraph= alt.Chart(df,width=1250, height=750).mark_area(interpolate="basis").encode(
	    alt.X('date:T',
	        axis=alt.Axis( domain=False, tickSize=0)
	    ),
	    alt.Y('count:Q', stack='center', axis=alt.Axis(labels=False, domain=False, tickSize=0)),
	    alt.Color('genre:N',
	        scale=alt.Scale(scheme='tableau20'),
	    ),tooltip=['genre','count']
	    
	).interactive().configure(background='#DDEEFF')
	streamgraph.save("list_stream.html")
	webbrowser.open('file://' + os.path.realpath("list_stream.html"))

def GenreStreamGraph():
	genres = []
	years = []
	counts = []
	db.query("SELECT COUNT(id) count, genre FROM library GROUP BY genre ORDER BY count DESC LIMIT 27;")
	
	for genre in db.rs:
 		genres.append(genre['genre'])

	data = []
	db.query("SELECT DISTINCT YEAR(date_added) year FROM library  ORDER BY year;")
	years = [item['year'] for item in db.rs]
	print("Gathering data... This might take a bit")
	for year in years:
		for month in range(1,13):
			for genre in genres:
				db.query("SELECT count(id) count FROM library WHERE genre = '" + genre + "' AND MONTH(date_added) = " + str(month) + " AND YEAR(date_added) = " + str(year)+ ";")
				for item in db.rs:

					if(month<10):
						s_month = "0" + str(month)
					else:
						s_month = str(month)
					date = str(year) + "-" + s_month #+ "-01T01:00:00.000Z"
					# print(date)
					data.append({"date": date, "genre":genre, "count": item['count']})
# , scale=alt.Scale(domain=(0,1000))

	df = pd.DataFrame(data=data)
	streamgraph= alt.Chart(df,width=1250, height=750).mark_area(interpolate="basis").encode(
	    alt.X('date:T',
	        axis=alt.Axis( domain=False, tickSize=0)
	    ),
	    alt.Y('count:Q', stack='center', axis=alt.Axis(labels=False, domain=False, tickSize=0)),
	    alt.Color('genre:N',
	        scale=alt.Scale(scheme='tableau20'),
	    ),tooltip=['genre','count']
	    
	).interactive().configure(background='#DDEEFF')
	streamgraph.save("lib_stream.html")
	webbrowser.open('file://' + os.path.realpath("lib_stream.html"))

def ArtistTreeMap():
	print("Be sure to close chart window before continuing")
	db.query("SELECT COUNT(id) as count, SUM(play_count) as pc, artist FROM library GROUP BY artist ORDER BY count DESC LIMIT 20;")

	sizs = []
	labels = []
	plays = []

	for genre in db.rs:
		sizs.append(genre['count'])
		labels.append(genre['artist'])
		plays.append(int(genre['pc']))

	# print(plays)

	# create a color palette, mapped to these values
	cmap = matplotlib.cm.Reds
	mini=min(plays)
	maxi=max(plays)
	norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
	colors = [cmap(norm(value)) for value in plays]
	 
	# Change color
	squarify.plot(sizes=sizs,label=labels, alpha=.8)#, color=colors )
	plt.axis('off')
	plt.show()

def GenreTreeMap():
	print("Be sure to close chart window before continuing")
	db.query("SELECT COUNT(id) as count, SUM(play_count) as pc, genre FROM library GROUP BY genre ORDER BY count DESC LIMIT 20;")

	sizs = []
	labels = []
	plays = []

	for genre in db.rs:
		sizs.append(genre['count'])
		labels.append(genre['genre'])
		plays.append(int(genre['pc']))

	# print(plays)

	# create a color palette, mapped to these values
	cmap = matplotlib.cm.Reds
	mini=min(plays)
	maxi=max(plays)
	norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
	colors = [cmap(norm(value)) for value in plays]
	 
	# Change color
	squarify.plot(sizes=sizs,label=labels, alpha=.8)#, color=colors )
	plt.axis('off')
	plt.show()


def StripPlot(year=None):
	print("Generating strip plot ...")
	#year - oldest year added for songs you want to look at, takes all songs if null
	db.query("SELECT count(record_id) count, genre FROM listening_history LEFT JOIN library on track_id = id GROUP BY genre ORDER BY count DESC LIMIT 10;")
	genres = []
	for item in db.rs:
		genres.append(item['genre'])
	songs = []

	max_play = 0
	for genre in genres:
		q = "SELECT name, artist, loved, genre, play_count, date_added FROM library WHERE  genre = '" + genre + "'"
		if year != None:
			q += " AND YEAR(date_added) > " + str(year) + ";"
		else:
			q += ";"
		db.query(q)
		
		for item in db.rs:
			if item['loved'] == 0:
				loved = False
			else:
				loved = True
			temp = {"name": item['name'],"artist":item['artist'], "genre": item['genre'].lower(), "play_count": item['play_count'],"loved":loved,"sk":item['date_added']}
			if(int(item['play_count']) > max_play):
				max_play = int(item['play_count'])

			songs.append(temp)

	if(max_play < 50):
		max_play = 50

	df = pd.DataFrame(data=songs)
	stripplot =  alt.Chart(df, width=100, height=500).mark_point(size=30,filled=True).encode(
	    x=alt.X(
	        'jitter:Q',
	        title=None,
	        axis=alt.Axis(values=[0], ticks=True, grid=False, labels=False),
	        scale=alt.Scale(),
	    ),
	    y=alt.Y('play_count:Q', scale=alt.Scale(domain=(0,max_play))),
	    color=alt.Color('loved:N',legend=None),tooltip=['name','artist','play_count'],
	    # size ='count:Q',
	    shape = alt.Shape(
	       "loved:N",
	        scale = alt.Scale(range=["circle", "triangle"],zero=True)),
	    #filled='true:B',
	    column=alt.Column(
	        'genre:N',
	        header=alt.Header(
	            labelAngle=-90,
	            titleOrient='top',
	            labelOrient='bottom',
	            labelAlign='right',
	            labelPadding=3,
	        ),
	        spacing=10,

	    ),
	).transform_calculate(
	    # Generate Gaussian jitter with a Box-Muller transform
	    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
	).configure_facet(
	    spacing=0
	).interactive().configure_view(
	    stroke=None
	)
	stripplot.save("StripPlot.html")
	webbrowser.open('file://' + os.path.realpath("StripPlot.html"))


# overall library growth over time
# command: lg
def LibGrowthChart():
	print("Gathering data... ")
	y = []
	x = []
	i = 0
	db.query("SELECT DISTINCT(YEAR(date_added)) yr FROM library ORDER BY yr;")
	years = [item['yr'] for item in db.rs]

	for year in years:
		for mo in range(1,12):

			# db.query("SELECT COUNT(id) count FROM library WHERE (YEAR(date_added) = " + str(year) + " AND MONTH(date_added) < " + str(mo) + ") OR YEAR(date_added) < " + str(year) + ";")
			# total = db.rs[0]['count']
			db.query("SELECT COUNT(id) count FROM library WHERE YEAR(date_added) = " + str(year) + " AND MONTH(date_added) = " + str(mo) + ";")
			count = db.rs[0]['count']
			
			# change = count - total

			x.append(year + mo/12)
			y.append(count)

	print("Be sure to close chart window before continuing.")
	plt.plot(x,y)
	plt.gcf().autofmt_xdate() 
	plt.show()

def CoronaGrowthChart():
	print("Gathering data... ")
	y = []
	x = []
	i = 0

	# db.query("SELECT COUNT(id) count FROM library WHERE (YEAR(date_added) = " + str(year) + " AND MONTH(date_added) < " + str(mo) + ") OR YEAR(date_added) < " + str(year) + ";")
	# total = db.rs[0]['count']
	db.query("SELECT count(id) count, DATE(date_added) date FROM library WHERE YEAR(date_added) = 2020 group by date ORder by date asc;")
	for item in db.rs:
		x.append(item['date'])
		y.append(item['count'])
	
		# change = count - total

		# x.append(2020+ mo/12)
		# y.append(count)

	print("Be sure to close chart window before continuing.")
	plt.plot(x,y)
	plt.gcf().autofmt_xdate() 
	plt.show()

#chart of overall listening history
#command: lc
def CoronaListenChart():
	y = []
	x = []
	print("Gathering data...")
	global db 
	db.query("SELECT COUNT(record_id) AS count, DATE(listen_date) AS date FROM listening_history WHERE YEAR(listen_date) > 2019 GROUP BY date ORDER BY date;")

	for date in db.rs:
		x.append(date['date'])
		y.append(date['count'])

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
		

def GenreGrowthChart():
	genres = []
	years = []
	counts = []
	db.query("SELECT COUNT(id) count, genre FROM library GROUP BY genre ORDER BY count DESC LIMIT 10;")
	
	for genre in db.rs:
 		genres.append(genre['genre'])

	data = []
	db.query("SELECT DISTINCT YEAR(date_added) year FROM library  ORDER BY year;")
	years = [item['year'] for item in db.rs]
	# years = [2020]
	for year in years:
		for month in range(1,12):
			if year == 2020 and month > 4:
				break;
			for genre in genres:
				db.query("SELECT count(id) count FROM library WHERE genre = '" + genre + "' AND MONTH(date_added) = " + str(month) + " AND YEAR(date_added) = " + str(year)+ ";")
				
				for item in db.rs:

					if(month<10):
						s_month = "0" + str(month)
					else:
						s_month = str(month)
					date = str(year)+ "-" + s_month + "T00:00:00.000Z"
					data.append({"date": date, "genre":genre, "count": item['count']})

	df = pd.DataFrame(data=data)
	print(df)
	lines = alt.Chart(df,width=1250, height=750).mark_line().encode(
	    x='date',
	    y='count',
	    color='genre',
	    # strokeDash='genre',
	    tooltip=['genre','count']
	).interactive()
	lines.save("genre_grow.html")
	webbrowser.open('file://' + os.path.realpath("genre_grow.html"))

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

# db.execute("Use MusicData")
# StripPlot()
# db.disconnect()


