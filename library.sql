CREATE DATABASE IF NOT EXISTS MusicData;
USE MusicData;


CREATE TABLE library (
	id INTEGER NOT NULL AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
	artist VARCHAR(50) DEFAULT NULL,
	album VARCHAR(50) DEFAULT NULL,
	album_artist VARCHAR(50) DEFAULT NULL,
	comp varchar(50) default null,
	genre varchar(50) default null,
	kind varchar(50) default null,
	total_time integer default null,
	track_num integer default null,
	track_count integer default null,
	year integer default null,
	date_mod datetime default null,
	play_count integer default null,
	play_date datetime default null,
	rel_date datetime default null,

	primary key (id);
);

CREATE TABLE listening_history (
	record_id integer not null auto_increment,
	track_id integer not null,
	listen_date datetime not null,

	primary key (record_id);
);