#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# EXTRA CREDIT includes: 
#           - bye handling for odd numbers of players
#           - repeat-match prevention
#           - draw handling, in reportMatch() and weighted rankings
#
# **NOTE** As the stubbed functions in the tournament.py provided for the
# project contained camelCase naming, the style has been maintained for 
# consistency although it is not in strict compliance with PEP8

import psycopg2
BYE = (9999,"BYE")


def pairHasPlayed(played, pair):
    '''Check if pairing is in list of previously played matches'''
    pairing = zip(sorted([pair[0],pair[1]]))
    pairing = str(pairing[:1])
    return (pairing in played) 


def connect(db_name="tournament"):
    '''Connect to PostgreSQL database. Returns database connection & cursor.'''
    # error handling, multi-object return per Udacity reviewer Zhe suggestion
    try:
        db = psycopg2.connect("dbname={}".format(db_name))
        return  db, db.cursor()
    except:
        print("Could not connect to database: tournament")
    

def deleteMatches():
    '''Remove all the match records from the database.'''
    conn, cur = connect()
    cur.execute("DELETE FROM match;")
    conn.commit()
    conn.close()


def deletePlayers():
    '''Remove all the player records from the database.'''
    conn, cur = connect()
    cur.execute("DELETE FROM player;")
    conn.commit()
    conn.close()


def countPlayers():
    '''Returns the number of players currently registered.'''
    conn, cur = connect()
    cur.execute( "SELECT COUNT(name) FROM player;")
    result = cur.fetchone()
    conn.close()
    # return int(result[0])
    return result[0]


def registerPlayer(name):
    '''Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.
  
    Args:
      name: the player's full name (need not be unique).
    '''
    conn, cur = connect()
    # add new player to player table
    cur.execute("INSERT INTO player (name) VALUES(%s);", (name, ))
    conn.commit()
    conn.close()


def playerStandings(option='default'):
    '''Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
      option: (optional) text argument to return a modified result set
        default - default values from project spec, see Returns below
        full - returns complete standings with losses, draws, and byes
        nobyes - returns standings for players who have not had a bye.
        seeding - returns standings ordered by weighted scoring for
                wins (3 pts), byes (2 pts) and draws (1pt)

    Returns: (default)
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    '''
    # connect to db
    conn, cur = connect()
    
    # define queries
    queries = dict()
    queries['default'] = ("SELECT player.id, player.name, "
                        "standings.wins, standings.matches "
                        "FROM player, standings WHERE player.id=standings.id "
                        "ORDER BY standings.wins DESC;")
    queries['full'] = ("SELECT player.id, player.name, "
                        "standings.wins, standings.losses, standings.draws, "
                        "standings.bye, standings.matches "
                        "FROM player, standings WHERE player.id=standings.id "
                        "ORDER BY standings.wins DESC, standings.losses;")
    queries['seeding'] = ("SELECT player.id, player.name "
                        "FROM player, seedings WHERE player.id=seedings.id "
                        "ORDER BY seedings.score DESC;")
    queries['nobyes'] = ("SElECT player.id, player.name "
                        "FROM player JOIN seedings ON player.id=seedings.id "
                        "WHERE player.bye=0 ORDER BY seedings.score DESC;")

    cur.execute(queries[option])
    standings = cur.fetchall()
    conn.close()
    return standings


def reportMatch(winner, loser=BYE[0], draw=0):
    '''Records the outcome of a single match between two players.

    Args:
      winner: id number of the player who won
      loser: (optional) id number of the player who lost,
         if not provided, the match is a BYE
      draw: (optional) 1 (or other truthy value) to indicate a draw or tie
    '''
    # connect to db
    conn, cur = connect()
    
    if draw:
        # add match to match table with no winner
        cur.execute("INSERT INTO match (wid, lid, draw) VALUES(%s, %s, TRUE);",
                (winner, loser))
    elif loser < BYE[0]:
        # add match to match table if the loser isn't the BYE id
        cur.execute("INSERT INTO match (wid, lid, draw) VALUES(%s, %s, FALSE);",
                    (winner, loser))
    else:
        # for byes, update the bye flag on the player record
        cur.execute("UPDATE player SET bye = 1 WHERE id = %s;", (winner,))

    # clean up connection
    conn.commit()
    conn.close()
 
 
def swissPairings():
    '''Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    
    This version handles byes for an odd number of registered players as well
    as draws(ties) and prevention of repeat matches. Rankings for pairings are
    ordered by weighted scoring for wins(3 pts), byes(2 pts), and draws(1pt).
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    '''
    # connect to db
    conn, cur = connect()
    round = []
    hasBye = False
   
    # check if BYE needed: player count must be even, so check modulo of 2
    if countPlayers() % 2:
        # get standings of players who haven't had a bye
        potentialByes = playerStandings('nobyes')
        # last place player gets the bye
        hasBye = potentialByes[-1]
        round.append(hasBye + BYE)

    # get played matches for in-memory check to prevent repeat matches
    cur.execute("SELECT wid, lid FROM match;")
    played = [sorted(pair) for pair in cur.fetchall()]
    played = [str(pair) for pair in played]

    # init lists
    newMatch = []
    bullpen = []
    
    # get standings
    standings = playerStandings('seeding')
    # if bye exists this round, remove player assigned to bye
    if hasBye: standings.remove(hasBye)
    # reverse order to use as stack 
    standings.reverse()
    
    # assign pairings from best to worse
    while standings:
        newMatch.append(standings.pop())  # first available player
        newMatch.append(standings.pop())  # next available player
        # check if match has been played before
        while pairHasPlayed(played, newMatch):
            bullpen.append(newMatch.pop())  # hold players to put back on stack
            newMatch.append(standings.pop()) 
        
        # flatten pairing to a single tuple and add to the round list
        round.append(newMatch[0] + newMatch[1])
        # return collisions back to stack
        bullpen.reverse()
        standings = standings + bullpen
        # clean up for next pass
        newMatch = []
        bullpen = []

    # clean up connection	
    conn.close()
    return round
