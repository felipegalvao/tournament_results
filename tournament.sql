-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players
(
  id serial NOT NULL PRIMARY KEY,
  name varchar(200)
);

CREATE TABLE matches
(
  id serial NOT NULL PRIMARY KEY,
  winner_id int references players(id),
  loser_id int references players(id)
);

-- create gamescounter view which joins matches and players tables to
-- count the number of matches by player.
CREATE VIEW matchescounter
AS
SELECT players.id,
       players.name,
       COUNT(matches.id) AS matches
FROM   players
       LEFT JOIN matches
              ON (players.id = matches.winner_id OR
                  players.id = matches.loser_id)
GROUP  BY players.id;

-- create wincounter view which joins matches and players tables to
-- count the number of wins by player.
CREATE VIEW wincounter
AS
SELECT players.id,
       players.name,
       COUNT(matches.winner_id) AS wins
FROM   players
       LEFT JOIN matches
              ON players.id = matches.winner_id
GROUP  BY players.id;

-- Create standings view, which joins the matchescounter and wincounter to
-- create the standings as required

CREATE VIEW standings
as
SELECT matchescounter.id,
       matchescounter.name,
       wincounter.wins,
       matchescounter.matches
FROM matchescounter
     JOIN wincounter
          ON matchescounter.id = wincounter.id
ORDER BY wincounter.wins desc;
