
                      Tournament Results/Planner
           Project 2 for Udacity Full Stack Web Dev NanoDegree


What is this?
-------------

This package contains a python module for managing players and results in a
Swiss style tournament. A database is configured and module functions handle
registering players, creating match pairings for a round of the tournament, and
recording results for each match played. In addition to the base requirements,
this implementation handles byes and draws and prevents re-matches.


Requirements
------------

 - Python 2.7 
 - PostgreSQL 9.3 or above
 - psycog2 2.4.5 or above
 
 
Installation
------------

Download or unpack the packaged files (see manifest below) to a folder in an
execution environment which includes Python 2.7 (2.7.9) and PostgreSQL 9.3 (or
above) such as in the Vagrant/VirtualBox VM provided for the project. Database
adapter psycopg2 must be installed in the Python environment.

Use PSQL to execute the tournament.sql command file to create the required
database, table, and views before running the tournament_test.py unit test 
program or the tourney_test extended text program.

Once the database is configured, either test program, tournament_test.py or
extended_tourney_test.py, can be run to verify module functions. To utilize all
module functions in another program, you must include the tournament.py file
and import the module:

	from tournament import *


File Manifest
-------------

The following files are included in this package:
 - README.txt - this file, documentation for the program/package
 - tournament.sql - SQL config commands to create database, tables, and views
 - tournament.py - module implementing required tournament functions
 - tournament_test.py - unit tests for the tournament functions (as provided)
 - extended_tourney_test.py - Extended text program requiring byes, generating
     draws, and processing multiple rounds (repeat match prevention)


Notes for the Reviewer
----------------------

In addition to the base requirements, the following extra credit features as
noted in the project description are implemented:
    - Prevent rematches
    - Support byes for an odd number of players; only one bye per player
    - Support draws
	
The ranking formula incorporating byes and draws assigns points as follows:
    Win = 3 points
    Bye = 2 points
    Draw = 1 point

This system values wins over real opponents slightly more than bye 'wins'.
(*Note: Points were hard-coded into the seedings view for expediency, but
  for a more robust implementation the points values could be referenced in 
  the view query calculations from a scoring config table. Out of scope here.)

*Extended Test program (extended_tourney_test.py):

    This program adds 15 players (sampling of Best Actor winners in 
    chronological order) to a tournament and then generates four (4) rounds of
    pairings and results. Full standings including wins, losses, draws, byes,
    and played matches are output after each round. 

    For each match, the player who is first alphabetically will normally win,
    however there is a 1 in 6 random chance any given match will end in a draw.
    Depending on the impact of random draws, final standings will usually
    approximate a roughly alpha sort by player name.

