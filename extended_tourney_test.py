#!/usr/bin/env python
#
# Extended test program for tournament.py extra credit features
# EXTRA CREDIT includes: 
#           - bye handling for odd numbers of players
#           - repeat-match prevention
#           - draw handling, in reportMatch() and weighted rankings
#  
# This program adds 15 players (sampling of Best Actor winners in chrono order)
# to a tournament and then generates four rounds of pairings and results. Full 
# standings are output after each round. For each match, the player who is
# first alphabetically will win, however there is a 1 in 6 random chance any
# given match will end in a draw. Depending on draw impact, final standings
# will usually roughly approximate an alpha sort on the player name.

import random
from tournament import *


def registerManyPlayers():
    '''Register 15 players (requiring a bye) for a tournament. '''
    registerPlayer("Emil Jannings")
    registerPlayer("Spencer Tracy")
    registerPlayer("Ronald Colman")
    registerPlayer("Alec Guinness")
    registerPlayer("Rod Steiger")
    registerPlayer("Richard Dreyfus")
    registerPlayer("Michael Douglas")
    registerPlayer("Tom Hanks")
    registerPlayer("Jack Nicholson")
    registerPlayer("Sean Penn")
    registerPlayer("Jamie Foxx")
    registerPlayer("Jeff Bridges")
    registerPlayer("Colin Firth")
    registerPlayer("Jean Dujardin")
    registerPlayer("Eddie Redmayne")


def pickwinners(pairs):
    '''Pick winners of matches with some random draws and reportMatch.'''
    for pair in pairs:
        if pair[2] < 9999:
            pair = sorted([pair[:2], pair[2:]],key=lambda player:player[1])
            pair = [x[0] for x in pair]
            draw = random.choice( [0,0,0,0,0,1])
            reportMatch(pair[0],pair[1], draw)
        else:
            reportMatch(pair[0])


if __name__ == '__main__':
    header = ["ID", "Name------", "Wins", "Losses", "Draws", "Byes", "Matches"]
    deleteMatches()
    deletePlayers()
    registerManyPlayers()
    
    print ("\n---Best Actor Tournament---")

    # run 4 rounds (min required number for tournament with this player count)
    for round in range(1,5): 
        pairings = swissPairings()
        pickwinners(pairings)
        
        #Print standings to console for test validation
        print "Round: " + str(round)
        standings = playerStandings('full')
        print('\t'.join(map(str,header)))
        for row in standings:
            print('\t'.join(map(str,row)))
