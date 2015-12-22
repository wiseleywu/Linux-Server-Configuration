-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop database IF EXISTS tournament;
drop sequence IF EXISTS number;
create database tournament;
\c tournament;
create table players(player_id serial primary key, name text);
create table matches(match_num integer,
                     player_id integer references players,
                     play_against integer references players,
                     wins integer,
                     points integer);
create sequence number;
