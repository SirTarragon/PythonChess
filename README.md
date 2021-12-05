# PythonChess
Authors:
Brandon Smith, Jose Ramirez, Tyler Pease, Tyler McLanahan

=========================================================

REQUIREMENTS:
At least Python 3.8.0

RUNNING:
If on Windows: Install Python through the Windows Store and then run the .bat file.
PYGAME is automatically installed through the .bat file.
This is recommended even if you use WSL.

If you're using WSL and don't want to run a .bat file, make sure you have a XServer
running on your machine for LINUX graphical applications.

If on LINUX:
Run the command: pip install PYGAME
Only run it if you don't already have PYGAME installed on your LINUX machine.
Otherwise just run the game.py script through python.

RUNNING THE SERVER:
Run the python script on another computer or a dedicated server. Make sure to modify the client.py script
to account for the IP address of the machine. The server is only capable of having two players on it
at a time.

=========================================================

VIDEO DEMONSTRATION:
https://youtu.be/WhFTBNQayJo

=========================================================

PROBLEM:
To develop a playable chess game without any game specific libraries through Python with several features. The features that were sought to be accomplished are listed below.
* Enable saving/loading of matches
* Ability to play against another person (on same or separate terminals)
* A clean and effective GUI system for visual representation of gameplay

INSTRUCTIONS FOR USER INTERFACE (OUTSIDE THE OBVIOUS):

LIST OF PYTHON LIBRARIES USED:
* pygame - for handling the graphical portions of the game
* sqlite3 - for the database
* datetime, time, sys, random, typing, copy, math, itertools, enum, socket, multiprocessing

EXTRA FEATURES IMPLEMENTED (BEYOND PROJECT PROPOSAL):

SEPARATION OF WORK:
The separation of work largely became highly mixed during the development of this project, below is the original separation of work from our project proposal submission:
* Jose Ramirez: Developing the chess game in Python to make it work, either with the use of the python-chess library if permitted or completely from scratch.  Will also help with developing elsewhere for the chess game as needed.

* Tyler Pease: Developing the General User Interface for the game itself – interfacing with the board to allow for better visibility, with potential move highlighting for visibility as well as helping with developing the chess game.

* Tyler McLanahan: Developing the saving and loading mechanics for the database – hopefully to save every move made by both black and white and to be able to load back to that state as well as helping with developing the chess game.

* Brandon Smith: Developing the capability of being able to easily revert moves by the player into a stack like Python-Chess as it may prove useful if able to be saved and for bug testing. Will do preliminary research into what we need for WebSockets to allow for two-player separate device playability, and will help with developing the chess game.
