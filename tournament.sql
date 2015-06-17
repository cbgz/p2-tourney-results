-- Table definitions for the tournament project.
--

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

-- player table: uses database serial for player ID (primary key), tracks whether a player has had a bye
CREATE TABLE player (
    id 		serial  PRIMARY KEY,	-- player unique ID
    name	text,					-- player full name
	bye		integer	DEFAULT 0		-- has player had bye (1): int instead of bool for simpler view math
);
-- Because this is a single tournament system (per base project spec), and when implementing byes, a player
-- may only have one buy, the condition of having had a bye is an attribute of the player. Byes could be
-- implemented in a separate table, but it would be a waste of tablespace within the scope of this spec.


-- match table: winner id (wid) and loser id (lid) constrained to registered players as foreign keys
CREATE TABLE match(
	m_id	serial  PRIMARY KEY,			-- match unique ID
	wid		integer references player(id),	-- winner player ID 
	lid		integer references player(id),	-- loser player ID
	draw	boolean							-- TRUE if match was a draw
);

-- View to calculate all totals for wins, losses, draws, byes, and matches played.
-- Filtered by queries in playerStandings() function to return desired values for different cases.	
CREATE VIEW standings AS
	SELECT
		player.id,
		SUM( CASE WHEN player.id = match.wid AND NOT match.draw THEN 1 ELSE 0 END) wins,
		SUM( CASE WHEN player.id = match.lid AND NOT match.draw THEN 1 ELSE 0 END) losses,
		SUM( CASE WHEN ((player.id = match.wid OR player.id = match.lid) AND match.draw) THEN 1 ELSE 0 END) draws,
		player.bye bye,
		SUM( CASE WHEN (player.id = match.wid OR player.id = match.lid) THEN 1 ELSE 0 END) matches
	FROM player LEFT JOIN match 
	ON (player.id = match.wid OR player.id = match.lid)
	GROUP BY player.id 
	ORDER BY wins DESC, draws, losses;
	
-- Separate seedings view to clarify ranking math; used hard-coded values but could have been
-- referenced instead from an additional table for configurability from program code. (out of scope)
CREATE VIEW seedings AS
	SELECT id, (3*wins + 2*bye + draws) score
	FROM standings
	ORDER BY score DESC, wins DESC;
	
