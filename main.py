# main.py
# Written by Elijah Wennberg-Smith
# Last Edited: 3.15.20
#
# This program controls Library Analyzer

import AnalysisLib as lib

def main():
	# listenChart()

	done = False
	print("Welcome to Library Anylizer")

	while(not done):

		u_input = input("Please enter Command: ").lower()
		if(u_input == "h"):
			print("    u - Update database from a specified XML file within the lib_backups/ directory.")
			print("   lg - Library growth chart over time")
			print("   lc - Listen chart over time")
			print("  tas - Top 10 artists by song count, pass integer to change list length.")
			print("sprob - songs ranked by skip probability.")
			print("gprob - genres ranked by skip probability.")
			print("aprob - artists ranked by skip probability.")
			print("    q - quit")

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
				i = input("Enter xml file: ")
				if(i != 'q'):
					lib.updateDBFromXML(file)

		elif(u_input == "lg"):
			lib.LibGrowthChart()
		elif(u_input == "lc"):
			lib.listenChart()
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

		elif(u_input == "q"):
			done = True



		else:
			print("Invalid command. enter " + '"' + 'h' + '"' + " for a list of commands.")



	print("Good Bye!")


main()



















