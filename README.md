# cube-timer-cli
Rubik's Cube Timer (command line interface)

## Dependencies

[pyTwistyScrambler](https://github.com/euphwes/pyTwistyScrambler) - Needed to generate scrambles

## Installation

	git clone 'https://github.com/Toory/cube-timer-cli'
	cd cube-timer-cli/src/
	svn export https://github.com/euphwes/pyTwistyScrambler/trunk/pyTwistyScrambler  # Download pyTwistyScrambler
	virtualenv env
	source ./env/bin/activate
	pip install -r requirements.txt #Download all dependencies needed
	sudo python cubetimer.py
	
Note that on Linux the script needs root permissions (required by the python module [keyboard](https://github.com/boppreh/keyboard))

## Usage
<p align="center"> 
  <img src="https://i.imgur.com/qa45CCR.gif">
</p>

In the file config.ini you can change each stat value to True/False (True = show, False = do not show)  

#### Main Menu:

    1. Timer.
    2. Print last solves.
    3. Delete all solves of a cube
    4. Import from Twisty Timer
    5. Exit.



1 - Go to the timer

2 - Print saved solves

3 - Delete all solves of a specific cube

4 - Import from a Twisty Timer backup file (android app)

5 - Exit the program

#### Timer:

	Choose cube type:
	 (1). One Handed
	 (2). 2x2
	 (3). 3x3
	 (4). 4x4
	 (5). 5x5
	 (6). 6x6
	 (7). 7x7
	 (b). Blind
	 (p). Pyraminx
	 (s1). Square-1
	 (s). Skewb
	 (c). Clock
	 (ctrl+c). Back to menu

You can choose the cube by inputting the number (or letter) on the parentheses.
This will be asked only on the first solve, after that the script will generate the scramble for the same cube,
until you go back to the main menu (ctrl+c) or exit the program.

After the scramble is generated you can:

    Start the Timer by pressing Enter
    Start the Inspection (if it's enabled in the config.ini file) by pressing Enter
    Go back to the main menu by pressing ctrl+c
    
If Inspection is Enabled the timer will start the countdown, you can:

    Stop the countdown and Start Solving by pressing Enter
    Stop the Timer without registering the solve by pressing Esc
    Go back to the main menu by pressing ctrl+c
    

After starting the timer you can:

    Stop the Timer by pressing Spacebar
    Stop the Timer without registering the solve by pressing Esc
    Go back to the main menu by pressing ctrl+c

All your solves will be saved in 'cubename_times.csv' (one file per every cube type).

## Credits

   [pyTwistyScrambler](https://github.com/euphwes/pyTwistyScrambler),
   [reddit.com/user/Storbod](https://github.com/Storbod/Python-Cube-Timer),
   [reddit.com/user/yovliporat](https://www.reddit.com/user/yovliporat)


	
