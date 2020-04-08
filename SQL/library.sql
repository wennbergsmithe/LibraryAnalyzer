CREATE TABLE library (
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
	name VARCHAR(255) NOT NULL,
	artist VARCHAR(255) DEFAULT 'No Artist',
	album VARCHAR(255) DEFAULT 'No Album',
	album_artist VARCHAR(255) DEFAULT 'No Album Artist',
	comp VARCHAR(255) DEFAULT 'No Composer',
	genre VARCHAR(255) DEFAULT 'No Genre',
	kind VARCHAR(255) DEFAULT 'No Kind',
	total_time INTEGER DEFAULT 0,
	track_num INTEGER DEFAULT 0,
	track_count INTEGER DEFAULT 0,
	year INTEGER DEFAULT 0,
	play_date DATETIME DEFAULT '1900-01-01',
	date_mod DATETIME DEFAULT '1900-01-01',
	play_count INTEGER DEFAULT NULL,
	rel_date DATETIME DEFAULT '1900-01-01',
	skip_count INTEGER DEFAULT 0,
	date_added DATETIME DEFAULT '1900-01-01'
);
CREATE INDEX idx ON library (artist);
CREATE TABLE listening_history (
	record_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	track_id INTEGER NOT NULL,
	listen_date DATETIME NOT NULL,
	listen_count INTEGER DEFAULT 0
);