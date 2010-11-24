create database mirvestigator;

# create user 'mirv'@'localhost' identified by <some password>;
# grant all privileges on mirvestigator.* to 'mirv'@'localhost';

create table jobs (
    uuid char(36) NOT NULL PRIMARY KEY,
    created_at datetime DEFAULT NULL,
    updated_at datetime DEFAULT NULL,
    status varchar(255)
);

create table parameters (
    job_uuid char(36) NOT NULL,
    key varchar(100) NOT NULL,
    value varchar(255) NOT NULL,
    INDEX (job_uuid)
);

create table pssms (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY
    position int NOT NULL,
    a float,
    t float,
    c float,
    g float
);

