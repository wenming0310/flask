PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS user;
CREATE TABLE user (
	id INTEGER PRIMARY KEY autoincrement,
	username VARCHAR(30) NOT NULL,
	password VARCHAR(30) NOT NULL,
	rank_id_FK INTEGER NOT NULL REFERENCES rank(id)
);

DROP TABLE IF EXISTS rank;
CREATE TABLE rank (
	id INTEGER PRIMARY KEY autoincrement,
	role_name VARCHAR(20) NOT NULL
);

DROP TABLE IF EXISTS entry;
CREATE TABLE entry (
	id INTEGER PRIMARY KEY autoincrement,
    slug VARCHAR(80) NOT NULL,
	title VARCHAR(80) NOT NULL,
	body TEXT NOT NULL,
	creation_date DATE NOT NULL,
	last_date DATE,
	user_id_FK INTEGER NOT NULL REFERENCES user(id)
);

DROP TABLE IF EXISTS entry_tags;
CREATE TABLE entry_tags (
	id_entry_FK INTEGER REFERENCES entry(id),
	id_tag_FK INTEGER REFERENCES tag(id),
	PRIMARY KEY(id_entry_FK, id_tag_FK)
);

DROP TABLE IF EXISTS tag;
CREATE TABLE tag (
	id INTEGER PRIMARY KEY autoincrement,
	name VARCHAR(10) NOT NULL
);

/* Sample data */
INSERT INTO "user" VALUES(1, 'bargio', 'f1b1a13033eddc3fdeecc0ed03bdc019c25890ba906658addad9fefe',0);
INSERT INTO "user" VALUES(2, 'test', '90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809',0);
INSERT INTO "user" VALUES(3, 'user', '90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809',1);
INSERT INTO "rank" VALUES(0,'administrator');
INSERT INTO "rank" VALUES(1,'user');

DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('rank',1);
INSERT INTO "sqlite_sequence" VALUES('user',1);
COMMIT;
