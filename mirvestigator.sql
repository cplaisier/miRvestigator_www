#create database mirvestigator;
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
    name varchar(100),
    value varchar(255),
    index(job_uuid)
);

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
    entrez_gene_id int,
    sequence varchar(12),
    start int,
    quality varchar(100),
    index(motif_id)
);

create table mirvestigator_scores (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    motif_id int NOT NULL,
    mirna_name varchar(100),              -- miRNA.name
    mirna_seed varchar(8),                -- miRNA.seed
    seedModel varchar(12),                -- model
    alignment varchar(100),               -- statePath
    viterbi_p float,                      -- vitPValue
    index(motif_id)
);

