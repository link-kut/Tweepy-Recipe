DROP TABLE userlist;
DROP TABLE nonkoreanuserlist;
DROP TABLE edgelist;

create table userlist(
   num INT NOT NULL AUTO_INCREMENT,
   userId VARCHAR(15) NOT NULL UNIQUE,
   name VARCHAR(200),
   screenName VARCHAR(200),
   numFollowers INT,
   lang VARCHAR(100),
   timeZone VARCHAR(100),
   location VARCHAR(200),
   fSamplingStatus VARCHAR(10) DEFAULT 'READY',
   PRIMARY KEY ( num )
);

create table nonkoreanuserlist(
   num INT NOT NULL AUTO_INCREMENT,
   userId VARCHAR(15) NOT NULL UNIQUE,
   friendId VARCHAR(15),
   name VARCHAR(200),
   screenName VARCHAR(200),
   lang VARCHAR(100),
   timeZone VARCHAR(100),
   location VARCHAR(200),
   PRIMARY KEY ( num )
);

create table edgelist(
   num INT NOT NULL AUTO_INCREMENT,
   followerId VARCHAR(15) NOT NULL,
   userId VARCHAR(15) NOT NULL,   
   PRIMARY KEY ( num )
);
