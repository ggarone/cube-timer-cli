"""
Credits:
	stats,getConfig,writeTime,readTimes based on code by https://www.reddit.com/user/Storbod
	https://github.com/Storbod/Python-Cube-Timer
	Scrambles are generated with pyTwistyScrambler
	https://github.com/euphwes/pyTwistyScrambler
	subx based on code by https://www.reddit.com/user/yovliporat
	https://drive.google.com/file/d/0B7qI7oJsiTPGcjY2VlpoQi1hLVU/view
"""
from pyTwistyScrambler import scrambler222, scrambler333, scrambler444,\
	scrambler555, scrambler666, scrambler777, squareOneScrambler, \
	pyraminxScrambler, skewbScrambler, clockScrambler
import datetime,time,fileinput
from collections import OrderedDict
from math import ceil, floor, sqrt
import csv
import os, sys
import configparser
import keyboard

class CubeTimer():

	def __init__(self):
		self.cubes_dict = {"1":"onehanded" , "2":"222" , "3":"333",
					  "b":"blindfolded" , "4":"444" , "5":"555",
					  "6":"666" , "7":"777" , "p":"pyra" ,
					  "s1":"square1" , "s":"skewb" , "c":"clock"}
		self.configValues = self.getConfig()
		self.cube = ''

		self.startCubeTimer()

	def startCubeTimer(self):
		while True:
			print('\x1b[0;35m-\x1b[0m'*30)
			print('\x1b[1;37;45m' + 'CUBE TIMER CLI'.center(30,' ') + '\x1b[0m')
			print('\x1b[0;35m-\x1b[0m'*30)
			try:
				print(f'1. Timer.\n2. Print last solves.\n3. Delete all solves of a cube\n4. Import from Twisty Timer\n5. Exit.\n'+'\x1b[0;35m-\x1b[0m'*30)
				userInput = int(input(">> "))
				if userInput == 1:
					self.timerMain()
				elif userInput == 2:
					self.printLastSolves()
				elif userInput == 3:
					self.deleteSolves()
				elif userInput == 4:
					self.ImportFromTwisty()
				elif userInput == 5:
					break
				else:
					print("Input was not valid.")
				self.cube = ''
			except Exception as e:
				print("Error: " + str(e))

	def timerMain(self):
		while True:
			try:
				self.ChooseCube()
				times,timestamps = self.GetStats()
				self.printStats(times, timestamps)
				scramble = self.GetScramble()
				print("[Press ctrl+c to Main Menu]\nPress Enter to start\n")
				keyboard.wait('enter')
				if self.configValues["inspectiontime"] != '0':
					print("[press esc to exit the inspection timer, Enter start solving]")
					self.inspectionTimer(self,self.configValues["inspectiontself,ime"])
				print("[Press ctrl+c to go Main Menu]\n[press esc to exit the timer]\nSpacebar to stop]")
				solve_time = self.Timer()
				#if timer was not stopped by user
				if solve_time != None:
					print("\x1b[6;30;42mTIME: {:^5.2f}\x1b[0m".format(solve_time))
					#if times is empty
					if not times:
						self.newBest()
					else:
						if solve_time < min(times):
							self.newBest()
					self.writeTime(solve_time,scramble)
				else:
					print("\nExiting timer...")
			except KeyboardInterrupt:
				print("\nExiting")
				break

	def printLastSolves(self):
		self.ChooseCube()
		times,timestamps = self.GetStats()
		self.PrintAoX(times,timestamps)

	def deleteSolves(self):
		'''
		Deletes all solves for a certain cube
		'''
		self.ChooseCube()
		with open(f'{self.cube}_times.csv', 'w') as f:
			f.write('')
		print(f'\x1b[0;32mAll solves from {self.cube} were deleted!\x1b[0m')

	def deleteLastSolve(self):
		#read content of file line by line
		with open(f'{self.cube}_times.csv', 'r') as fin:
			lines = fin.readlines()
			f.close()
		#write all lines except last line (last solve)
		with open(f'{self.cube}_times.csv', 'w') as fout:
			fout.writelines([line for line in lines[-1]])
			fout.close()

	def ChooseCube(self):
		if self.cube == '':
			print(
			'Choose cube type:\n',\
			'(1). One Handed\n',\
			'(2). 2x2\n',\
			'(3). 3x3\n',\
			'(4). 4x4\n',\
			'(5). 5x5\n',\
			'(6). 6x6\n',\
			'(7). 7x7\n',\
			'(b). Blind\n',\
			'(p). Pyraminx\n',\
			'(s1). Square-1\n',\
			'(s). Skewb\n',\
			'(c). Clock\n',\
			'(ctrl+c). Back to menu')
			userInput = input(">> ")
			self.cube = self.cubes_dict[userInput]

	def getConfig(self):
		configValues = dict()
		config = configparser.ConfigParser()
		config.read("config.ini")
		for key in config["DEFAULT"]:
			configValues[key] = config["DEFAULT"][key]
		
		return configValues

	def writeTime(self,time,scramble):
		with open("{}_times.csv".format(self.cube), "a", newline="") as times:
			writer = csv.writer(times)
			writer.writerow([time , datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') , scramble])

	def readTimes(self):
		times, timestamps = [], []
		with open("{}_times.csv".format(self.cube), newline = "") as saveFile:
			reader = csv.reader(saveFile, delimiter=",")
			for row in reader:
				times.append(row[0])
				timestamps.append(row[1])

		times = [float(time) for time in times]
		return times, timestamps

	def Timer(self):
		minutes = 0
		seconds = 0
		millis = 0

		while True:
			sys.stdout.write(f"\r{minutes}::{seconds}::{millis}")
			sys.stdout.flush()
			millis += 10

			if (millis % 500) != 0:
				time.sleep(0.01)

			if millis >= 1000:
				seconds += 1
				millis = 0

			if seconds >= 60:
				minutes += 1
				seconds = 0

			#if spacebar is pressed stop timer
			if keyboard.is_pressed(' '):
				break 
			#if esc is pressed exit timer
			if keyboard.is_pressed('esc'):
				return

		print("\n")
		solve_time = (minutes * 60000 + seconds * 1000 + millis) / 1000
		return solve_time

	def inspectionTimer(self,insptime):
		time.sleep(0.1)
		secs = int(insptime)
		"""starts at 900 milliseconds instead of 1000 because of the sleep
		needed to avoid conflict when pressing the 'enter' key"""
		millis = 900

		while secs:
			sys.stdout.write("\r{}::{}".format(secs,millis))
			millis -= 10

			if (millis % 500) != 0:		
				time.sleep(0.01)

			#make a beep sound at 8 and 12 seconds
			if secs == 7 and millis == 0 or secs == 3 and millis == 0:
				print ("\a", end='')
			if millis <= 0:
				secs -= 1
				millis = 1000
			if keyboard.is_pressed('enter'):
				break 
			if keyboard.is_pressed('esc'):
				return
		print('\nStart Solving!\n')
		
	def newBest(self):
		print("""
	  _   _   ______  __          __    ____    ______    _____   _______   _ 
	 | \ | | |  ____| \ \        / /   |  _ \  |  ____|  / ____| |__   __| | |
	 |  \| | | |__     \ \  /\  / /    | |_) | | |__    | (___      | |    | |
	 | . ` | |  __|     \ \/  \/ /     |  _ <  |  __|    \___ \     | |    | |
	 | |\  | | |____     \  /\  /      | |_) | | |____   ____) |    | |    |_|
	 |_| \_| |______|     \/  \/       |____/  |______| |_____/     |_|    (_)
		""")

	def getBest(self,num,times,timeslen):
		index=0
		Best = 1000.00
		for index in range(index,timeslen-(num-2)):
			lastTimes = times[index:index+num-1]
			if num == 5 or num == 12:
				lastTimes.pop(lastTimes.index(max(lastTimes)))
				lastTimes.pop(lastTimes.index(min(lastTimes)))
			elif num == 50:
				for i in range(0,3):
					lastTimes.pop(lastTimes.index(max(lastTimes)))
					lastTimes.pop(lastTimes.index(min(lastTimes)))
			elif num == 100:
				for i in range(0,5):
					lastTimes.pop(lastTimes.index(max(lastTimes)))
					lastTimes.pop(lastTimes.index(min(lastTimes)))
			elif num == 1000:
				for i in range(0,50):
					lastTimes.pop(lastTimes.index(max(lastTimes)))
					lastTimes.pop(lastTimes.index(min(lastTimes)))
			sumLastTimes = sum(lastTimes)
			CurrentBest = round(sumLastTimes / len(lastTimes), 3)
			if(CurrentBest < Best):
				Best = CurrentBest
		print("\tAo{:<4}: {:^5.2f}".format(num,Best))

	def getCurrent(self,num,times,timeslen):
		lastTimes = times[-num:]
		if num == 5 or num == 12:
			lastTimes.pop(lastTimes.index(max(lastTimes)))
			lastTimes.pop(lastTimes.index(min(lastTimes)))
		elif num == 50:
			for i in range(0,3):
				lastTimes.pop(lastTimes.index(max(lastTimes)))
				lastTimes.pop(lastTimes.index(min(lastTimes)))
		elif num == 100:
			for i in range(0,5):
				lastTimes.pop(lastTimes.index(max(lastTimes)))
				lastTimes.pop(lastTimes.index(min(lastTimes)))
		elif num == 1000:
			for i in range(0,50):
				lastTimes.pop(lastTimes.index(max(lastTimes)))
				lastTimes.pop(lastTimes.index(min(lastTimes)))
		sumLastTimes = sum(lastTimes)
		CurrentBest = round(sumLastTimes / len(lastTimes), 3)
		print("Ao{:<4}: {:^5.2f}".format(num,CurrentBest), end="")

	def printStats(self,times,timestamps):
		timeslen = len(times)

		print('\x1b[0;34m-\x1b[0m'*30)
		print('\x1b[1;37;44m' + 'TIMER'.center(30,' ') + '\x1b[0m')
		print('\x1b[0;34m-\x1b[0m'*30)

		if self.configValues["solves"] == "True":
			print("\tSolves: " + str(timeslen))
			print('\x1b[0;34m-\x1b[0m'*30)

		if timeslen >= 1:
			if self.configValues["subx"] == "True":
				timeKeys = self.configValues["timekeys"].split(",")
				timeKeys = [int(key) for key in timeKeys]
				dictonary = OrderedDict()
				
				for value in timeKeys:
					dictonary[float(value)] = 0
			
				for key in dictonary.keys():
					for time in times:
						if time < key:
							dictonary[key] += 1
					
				for key, val in dictonary.items():
					print("Sub-{:^5}:{:^5}[{:^5}%]".format(str(key), str(val), str(float(val) / float(len(times)) * 100.0)[:5]))
				print('\x1b[0;34m-\x1b[0m'*30)
		
		print("  Current\t    Best\n" + '\x1b[0;34m-\x1b[0m'*30)
		if timeslen >= 3:
			if self.configValues["ao3"] == "True":
				self.getCurrent(3,times,timeslen)
				self.getBest(3,times,timeslen)
			if timeslen >= 5:
				if self.configValues["ao5"] == "True": 
					self.getCurrent(5,times,timeslen)
					self.getBest(5,times,timeslen)
				if timeslen >= 12:
					if self.configValues["ao12"] == "True":
						self.getCurrent(12,times,timeslen)
						self.getBest(12,times,timeslen)
					if timeslen >= 50:
						if self.configValues["ao50"] == "True":
							self.getCurrent(50,times,timeslen)
							self.getBest(50,times,timeslen)
						if timeslen >= 100:
							if self.configValues["ao100"] == "True":
								self.getCurrent(100,times,timeslen)
								self.getBest(100,times,timeslen)
							if timeslen >= 1000:
								if self.configValues["ao1000"] == "True":
									self.getCurrent(1000,times,timeslen)
									self.getBest(1000,times,timeslen)
		print('\x1b[0;34m-\x1b[0m'*30)
		if timeslen >= 2:
			if self.configValues["mean"] == "True":
				totalTime = sum(times)
				print("{:8}{:6.2f}".format('Mean:',round(totalTime / len(times), 3)))

			if self.configValues["median"] == "True":
				sortedTimes = sorted(times)
				if len(sortedTimes) % 2 == 0:
					median = round(sortedTimes[ceil(len(sortedTimes) / 2)], 3)
				else:
					median = round((sortedTimes[floor(len(sortedTimes) / 2)] + sortedTimes[ceil(len(sortedTimes) / 2)]) / 2, 3)
				print("{:8}{:6.2f}".format('Median:',median))

			if self.configValues["standarddeviation"] == "True":
				average = sum(times) / len(times)
				deviations = [(x - average) ** 2 for x in times]
				variance = sum(deviations) / len(deviations)
				standardDeviation = sqrt(variance)
				print("{:8}{:6.2f}".format('SD:',round(standardDeviation, 3)))
		
		if timeslen >= 1:
			if self.configValues["best"] == "True":
				print("{:8}{:6.2f}".format('Best:',min(times)))
				
			if self.configValues["worst"] == "True":
				print("{:8}{:6.2f}".format('Worst:',max(times)))
			
			if self.configValues["latest"] == "True":
				print("{:8}{:6.2f}".format('Last:',times[-1]))

	def GetScramble(self):
		self.ChooseCube()

		if self.cube == "222":   
			scramble = scrambler222.get_WCA_scramble() 
		elif self.cube == "333" or self.cube == "onehanded" or self.cube == "blindfolded":	
			scramble = scrambler333.get_WCA_scramble()
		elif self.cube == "444":	
			scramble = scrambler444.get_WCA_scramble(n=40)
		elif self.cube == "555":	
			scramble = scrambler555.get_WCA_scramble(n=60)
		elif self.cube == "666":
			scramble = scrambler666.get_WCA_scramble(n=80)
		elif self.cube == "777":
			scramble = scrambler777.get_WCA_scramble(n=100)
		elif self.cube == "pyraminx":
			scramble = pyraminxScrambler.get_WCA_scramble()
		elif self.cube == "square1":
			scramble = squareOneScrambler.get_WCA_scramble()
		elif self.cube == "skewb":
			scramble = skewbScrambler.get_WCA_scramble()
		elif self.cube == "clock":
			scramble = clockScrambler.get_WCA_scramble()
		else:
			print("Didn't recognize input, assuming 3x3 ..")
			scramble = scrambler333.get_WCA_scramble()

		print("\n" + scramble + "\n")
		return scramble

	def PrintAoX(self,times,timestamps):
		try:
			if not times:
				#if the there are no recorded solves
				raise ValueError("No recorded solves.")
			lastTimes = times[-20:]
			lastTimestamps = timestamps[-20:]
			for i in range(20):
				if i >= len(lastTimes):
					break
				print(f"{lastTimestamps[i]} {lastTimes[i]:.2f} ")
			input("Press Enter to continue...")
		except IndexError:
			print("Error, index no recorded solves.")
		except Exception as e:
			print("\x1b[0;31mError: \x1b[0m" + str(e))

	def GetStats(self):
		try:
			times, timestamps = [], []
			#if file it's not empty
			if(os.stat("{}_times.csv".format(self.cube)).st_size != 0):
				times, timestamps = self.readTimes()
		except IndexError:
			print("Error, no recorded solves.")
		except FileNotFoundError:
			print("File \"{}_times.csv\" not found, creating new one".format(self.cube))
			file = open(f"{self.cube}_times.csv", 'w+')
		except Exception as e:
			print("\x1b[0;31mError: \x1b[0m" + str(e))

		return times,timestamps

	def ImportFromTwisty(self):
		Filein = input("Input filename of twisty timer backup.\n>> ")
		with open(Filein, "r", newline="") as times:
			for line in times:
				cube = line.split('"')
				cubetype = str(*cube[1:2])
				for key,value in self.cubes_dict.items():
					if cubetype == value:
						cube[-1] = cube[-1].strip()
						solve = float(*cube[5:6]) / 1000
						epoch = int(*cube[7:8]) / 1000
						scramble = str(*cube[9:10])
						solve_time = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
						file = open("{}_times.csv".format(cubetype),"a", newline="")
						print("{},{},{}".format(solve,solve_time,scramble), file=file)

if __name__ == '__main__':
	CubeTimer()
