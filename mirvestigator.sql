-- @Program: miRvestigator
-- @Version: 2
-- @Author: Chris Plaisier
-- @Author: Christopher Bare
-- @Sponsored by:
-- Nitin Baliga, ISB
-- Institute for Systems Biology
-- 1441 North 34th Street
-- Seattle, Washington  98103-8904
-- (216) 732-2139
-- @Also Sponsored by:
-- Luxembourg Systems Biology Grant

-- If this program is used in your analysis please mention who
-- built it. Thanks. :-)

-- Copyright (C) 2010 by Institute for Systems Biology,
-- Seattle, Washington, USA.  All rights reserved.

-- This source code is distributed under the GNU Lesser
-- General Public License, the text of which is available at:
--   http://www.gnu.org/copyleft/lesser.html

-- create database mirvestigator;
-- create user 'mirv'@'localhost' identified by <some password>;
-- grant all privileges on mirvestigator.* to 'mirv'@'localhost';
-- use mirvestigator;

drop table if exists jobs;
drop table if exists parameters;
drop table if exists genes;
drop table if exists motifs;
drop table if exists pssms;
drop table if exists sites;
drop table if exists mirvestigator_scores;
drop table if exists species;

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
    entrez_id varchar(20),
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
    position int,
    a float,
    t float,
    c float,
    g float,
    index(motif_id)
);

create table sites (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    motif_id int NOT NULL,
    sort_order int,
    entrez_gene_id varchar(20),
    sequence varchar(20),
    start int,
    quality varchar(100),
    mfe varchar(50),
    index(motif_id)
);

create table mirvestigator_scores (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    motif_id int NOT NULL,
    sort_order int,
    mirna_name varchar(2000),              -- miRNA.name
    mirna_seed varchar(8),                -- miRNA.seed
    seedModel varchar(20),                -- model
    alignment varchar(100),               -- statePath
    viterbi_p float,                      -- vitPValue
    index(motif_id)
);

create table gene_identifiers (
    species varchar(20),
    id_type varchar(20),
    identifier varchar(100),
    entrez_id varchar(20),
    index(identifier),
    index(species, id_type, identifer),
    index(entrez_id)
);

create table species (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(100),
    ucsc_name varchar(100),
    ncbi_id int,
    mirbase varchar(10),
    weeder varchar(10),
    index(mirbase)
);

-- populate species lookup table
insert into species (name, ucsc_name, ncbi_id, mirbase, weeder) values('D. melanogaster', 'Drosophila_melanogaster', 7227, 'dme', 'DM3P');
insert into species (name, ucsc_name, ncbi_id, mirbase, weeder) values('G. gallus',       'Gallus_gallus',           9031, 'gga', 'GG3P');
insert into species (name, ucsc_name, ncbi_id, mirbase, weeder) values('R. novergicus',   'Rattus_norvegicus',      10116, 'rno', 'RN3P');
insert into species (name, ucsc_name, ncbi_id, mirbase, weeder) values('H. sapiens',      'Homo_sapiens',            9606, 'hsa', 'HS3P');
insert into species (name, ucsc_name, ncbi_id, mirbase, weeder) values('C. elegans',      'Caenorhabditis_elegans',  6239, 'cel', 'CE3P');
insert into species (name, ucsc_name, ncbi_id, mirbase, weeder) values('C. familiaris',   'Canis_familiaris',        9615, 'cfa', 'CF3P');
insert into species (name, ucsc_name, ncbi_id, mirbase, weeder) values('M. musculus',     'Mus_musculus',           10090, 'mmu', 'MM3P');
insert into species (name, ucsc_name, ncbi_id, mirbase, weeder) values('D. rerio',        'Danio_rerio',             7955, 'dre', 'DR3P');


