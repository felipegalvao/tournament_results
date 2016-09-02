#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect(database_name="tournament"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")

def deleteMatches():
    """Remove all the match records from the database."""
    DB, c = connect()

    c.execute("DELETE FROM matches")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB, c = connect()

    c.execute("DELETE FROM players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB, c = connect()

    c.execute("SELECT COUNT(*) FROM players")
    number_of_players = int(c.fetchone()[0])
    return(number_of_players)

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect()

    c.execute("INSERT INTO players (name) values(%s)",(bleach.clean(name),))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, c = connect()

    c.execute("SELECT * FROM standings")
    players_standings = c.fetchall()
    return(players_standings)

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, c = connect()

    c.execute("INSERT INTO matches (winner_id, loser_id) values (%s,%s)",(winner,loser,))
    DB.commit()
    DB.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Return players standings and number of players
    player_standings = playerStandings()
    num_of_players = countPlayers()
    list_of_pairings = []

    # Pair the players based on the standings, which is already sorted by wins
    for i in xrange(0,num_of_players,2):
        pairing_tuple = (player_standings[i][0], player_standings[i][1],
                         player_standings[i+1][0], player_standings[i+1][1])
        list_of_pairings.append(pairing_tuple)
    return(list_of_pairings)
