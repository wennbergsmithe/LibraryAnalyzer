# main.py
# Written by Elijah Wennberg-Smith
# Last Edited: 3.26.20
#
# This program controls Library Analyzer

import AnalysisLib as lib
import PlaylistLib as plib
from globals import db

db_name = ""

def main():
	done1 = False
	done2 = False
	print("Welcome to Library Anylizer")

	while(not done1):
		db_name = input("Enter the database name to login or create. q to quit: ")
		if(db_name == "q"):
			done1 = True
			done2 = True
		else:	
			if db.changeDB(db_name) == -1:
				make = "z"
				while(make != "y" and make != "n"):
					make = input("This database does not exist. Would you like to create it? (y)es or (n)o: ")
					if(make == "y"):
						db.newDB(db_name)
						done1 = True
						break
					elif(make == "n"):
						continue
					else:
						print("enter y or n.")
			else:
				done1 = True

	while(not done2):

		u_input = input("Please enter Command or h for a list of commands: ").lower()
		if(u_input == "h"):
			print()
			print("Database commands:")
			print("  u ------- Update database from a specified XML file within the lib_backups/ directory.")
			print("  e ------- Execute database command (no queries).")
			print()
			print("Charts:")
			print("  lg ------ Library growth chart over time.")
			print("  lc ------ Listen chart over time.")
			print("  monchar - Chart of total number of songs by month.")
			print("  sgp ----- Genre stream graph by plays.")
			print("  sg ------ Genre stream graph by songs in library.")
			print("  strip --- Song playcount strip plot by genre.")
			print("  gtmap --- Top 20 genre tree map.")
			print("  atmap --- Top 20 artist tree map.")
			print()
			print("Lists:")
			print("  tas ----- Top 10 artists by song count, pass integer to change list length.")
			print("  sprob --- Songs ranked by skip probability.")
			print("  gprob --- Genres ranked by skip probability.")
			print("  aprob --- Artists ranked by skip probability.")
			print("  sby ----- Top 10 songs by plays, pass integer to change list length.")
			print("  gbs ----- Top ten genres by number of songs, pass int to change list length.")
			print("  sbp ----- Top ten songs by number of plays, pass int to change list length.")
			print()
			print("Playlists:")
			print("  uplay --- Generates a playlist of unheard songs - optional pass genre and year")
			print()
			print("Program:")
			print("  q ------- Quit")
			print()

		
		elif(u_input == "lg"): #lib growth chart
			lib.LibGrowthChart()

		elif(u_input == "lc"): #listen chart over time
			lib.listenChart()
		elif(u_input == "sgp"):
			lib.GenreStreamGraphPlays()
		elif(u_input == "sg"):
			lib.GenreStreamGraph()
		elif(u_input[:3] == "tas"): 
			if(len(u_input) > 3):
				if(u_input.find(" ") == -1):
					print("your command is whack")
					continue
				else:	
					try:
						x = int(u_input[u_input.find(" ") + 1:])
					except ValueError :
						print("invalid list length")
					else:
						if(x > 0):
							lib.TopXArtistsBySongs(x)
						else:
							print("invalid list length")
			else:
				lib.TopXArtistsBySongs()

		elif(u_input[:5] == "sprob"):
			if(len(u_input) > 5):
				if(u_input.find(" ") == -1):
					print("your command is whack")
					continue
				else:	
					try:
						args = u_input.split(" ")
						x = int(args[1])
					except ValueError :
						print("invalid list length")
					else:
						if(x > 0):
							if (len(args) == 3):
								lib.SongSkipProbability(x=x,asc=int(args[2]))
							elif(len(args) == 4):
								lib.SongSkipProbability(x=x,asc=int(args[2]),zeros_ones=int(args[3]))
							else:
								lib.SongSkipProbability(x=x)
						else:
							print("invalid list length")
			else:
				lib.SongSkipProbability(10)
		elif(u_input == "strip"):
			lib.StripPlot()

		elif(u_input[:5] == "gprob"):
			if(len(u_input) > 5):
				if(u_input.find(" ") == -1):
					print("your command is whack")
					continue
				else:	
					try:
						args = u_input.split(" ")
						x = int(args[1])
					except ValueError :
						print("invalid list length")
					else:
						if(x > 0):
							if (len(args) == 3):
								lib.GenreSkipProbability(x=x,asc=int(args[2]))
							elif(len(args) == 4):
								lib.GenreSkipProbability(x=x,asc=int(args[2]),zeros_ones=int(args[3]))
							else:
								lib.GenreSkipProbability(x=x)
						else:
							print("invalid list length")
			else:
				lib.GenreSkipProbability(10)

		elif(u_input[:5] == "aprob"):
			if(len(u_input) > 5):
				if(u_input.find(" ") == -1):
					print("your command is whack")
					continue
				else:	
					try:
						args = u_input.split(" ")
						x = int(args[1])
					except ValueError :
						print("invalid list length")
					else:
						if(x > 0):
							if (len(args) == 3):
								lib.ArtistSkipProbability(x=x,asc=int(args[2]))
							elif(len(args) == 4):
								lib.ArtistSkipProbability(x=x,asc=int(args[2]),zeros_ones=int(args[3]))
							else:
								lib.ArtistSkipProbability(x=x)
						else:
							print("invalid list length")
			else:
				lib.ArtistSkipProbability(10)


		elif(u_input[:3] == "sby"): 
			if(len(u_input) > 3):
					if(u_input.find(" ") == -1):
						print("your command is whack")
						continue
					else:	
						try:
							x = int(u_input[u_input.find(" ") + 1:])
						except ValueError :
							print("invalid list length")
						else:
							if(x > 0):
								lib.NumSongsByYear(x)
							else:
								print("invalid list length")
			else:
				lib.NumSongsByYear()
		elif(u_input == "monchar"):
			lib.MonthsBySongsAdded()
		elif(u_input[:3] == "gbs"): 
			if(len(u_input) > 3):
					if(u_input.find(" ") == -1):
						print("your command is whack")
						continue
					else:	
						try:
							x = int(u_input[u_input.find(" ") + 1:])
						except ValueError :
							print("invalid list length")
						else:
							if(x > 0):
								lib.TopXGenresBySongs(x)
							else:
								print("invalid list length")
			else:
				lib.TopXGenresBySongs()
		elif(u_input == "gtmap"):
			lib.GenreTreeMap()
		elif(u_input == "atmap"):
			lib.ArtistTreeMap()
		elif(u_input[:3] == "sbp"): 
			if(len(u_input) > 3):
					if(u_input.find(" ") == -1):
						print("your command is whack")
						continue
					else:	
						try:
							x = int(u_input[u_input.find(" ") + 1:])
						except ValueError :
							print("invalid list length")
						else:
							if(x > 0):
								lib.TopXSongsByPlays(x)
							else:
								print("invalid list length")
			else:
				lib.TopXSongsByPlays()


		elif(u_input[:5] == "uplay"):
			print("here")
			if(len(u_input) > 5):
				if(u_input.find(" ") == -1):
					print("your command is whack")
					continue
				else:	
					try:
						args = u_input.split(" ")
						x = int(args[1])
					except ValueError :
						print("invalid list length")
					else:
						if(x > 0):
							if (len(args) == 3):
								plib.PlayListUnheard(db_name, x=x,genre=args[2])
							elif(len(args) == 4):
								plib.PlayListUnheard(db_name,x=x, genre=args[2],since=int(args[3]))
							else:
								plib.PlayListUnheard(db_name,x=x)
						else:
							print("invalid list length")
			else:
				plib.PlayListUnheard(db_name, x=10)

		elif(u_input[0] == "u"):
			if(len(u_input) > 1):
				if(u_input.find(" ") == -1):
					print("your command is whack")
					continue
				else:	
					arg = u_input[u_input.find(" ") + 1:]
					print(arg)
					lib.updateDBFromXML(arg)
			else:
				i = input("Enter xml file or q to quit: ")
				if(i != 'q'):
					lib.updateDBFromXML(i)



		elif(u_input[:5] == "newdb"):
			if(len(u_input) > 5):
				if(u_input.find(" ") == -1):
					print("your command is whack")
					continue
				else:	
					arg = u_input[u_input.find(" ") + 1:]
					print(arg)
					db.newDB(arg)
			else:
				i = input("Enter new database name or q to quit: ")
				if(i != 'q'):
					db.newDB(i)

		elif(u_input == "e"):
			ui = input("Enter SQL command or q to quit. (no queries, commands only): ")
			if(ui!= "q"):
				db.execute(ui)

		elif(u_input == "q"):
			done2 = True
		else:
			print("Invalid command. enter " + '"' + 'h' + '"' + " for a list of commands.")



	print("Good Bye!")

# # db = DBConnector()
main()
db.disconnect()


















