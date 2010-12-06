#create database mirvestigator;
# create user 'mirv'@'localhost' identified by <some password>;
# grant all privileges on mirvestigator.* to 'mirv'@'localhost';

drop table if exists jobs;
drop table if exists parameters;
drop table if exists genes;
drop table if exists motifs;
drop table if exists pssms;
drop table if exists sites;
drop table if exists mirvestigator_scores;

create table jobs (
    uuid char(36) NOT NULL PRIMARY KEY,
    created_at datetime DEFAULT NULL,
    updated_at datetime DEFAULT NULL,
    status varchar(255),
    status_message varchar(1000)
);

create table parameters (
    job_uuid char(36) NOT NULL,
    name varchar(100),
    value varchar(255),
    index(job_uuid)
);

# name is the entrez id of the gene
# sequence indicates whether sequence for this gene exists
# in file extracted from genbank
create table genes (
    job_uuid char(36) NOT NULL,
    name varchar(100),
    sequence boolean,
    index(job_uuid)
);

create table motifs (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    job_uuid char(36) NOT NULL,
    name varchar(100),
    score float
);

create table pssms (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    motif_id int NOT NULL,
    a float,
    t float,
    c float,
    g float,
    index(motif_id)
);

create table sites (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    motif_id int NOT NULL,
    entrez_gene_id varchar(20),
    sequence varchar(20),
    start int,
    quality varchar(100),
    index(motif_id)
);

create table mirvestigator_scores (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    motif_id int NOT NULL,
    mirna_name varchar(2000),              -- miRNA.name
    mirna_seed varchar(8),                -- miRNA.seed
    seedModel varchar(20),                -- model
    alignment varchar(100),               -- statePath
    viterbi_p float,                      -- vitPValue
    index(motif_id)
);

