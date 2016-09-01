-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players
(
  id serial NOT NULL PRIMARY KEY,
  name varchar(200),
  wins int,
  matches int
);

CREATE TABLE matches
(
  winner_id int references players(id),
  loser_id int references players(id)
);
