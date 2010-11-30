#
# Interact with the mirvestigator MySQL database
#

import MySQLdb
import datetime
import time


def _get_db_connection():
    return MySQLdb.connect("localhost","mirv","mirvestigator","mirvestigator")


def create_job_in_db(job):
    conn = _get_db_connection()
    try:
        created_at = datetime.datetime.now()
        cursor = conn.cursor()

        job_uuid = job['id']
        
        cursor.execute("insert into jobs (uuid, created_at, updated_at, status) values ('%s', '%s', '%s', '%s');"
                       % (job_uuid, created_at.isoformat(), created_at.isoformat(), 'queued'))
        for k, v in job.iteritems():
            if k!='id':
                cursor.execute("insert into parameters (job_uuid, name, value) values (%s, %s, %s);",
                               (job_uuid, k, str(v),) )
    finally:
        try:
            cursor.close()
        except Exception as exception:
            print("Exception closing cursor: ")
            print(exception)
        try:
            conn.close()
        except Exception as exception:
            print("Exception closing conection: ")
            print(exception)


def get_job_status(job_uuid):
    conn = _get_db_connection()
    try:
        created_at = datetime.datetime.now()
        cursor = conn.cursor()
        cursor.execute("select * from jobs where uuid=%s;", (job_uuid,))
        row = cursor.fetchone()
        created_at = row[1];
        updated_at = row[2];
        status = row[3];
        return (created_at, updated_at, status,)
    finally:
        try:
            cursor.close()
        except Exception as exception:
            print("Exception closing cursor: ")
            print(exception)
        try:
            conn.close()
        except Exception as exception:
            print("Exception closing conection: ")
            print(exception)


def update_job_status(job_uuid, status):
    conn = _get_db_connection()
    try:
        now = datetime.datetime.now()
        cursor = conn.cursor()
        cursor.execute("update jobs set status='%s', updated_at='%s' where uuid='%s';"
                       % (status, now.isoformat(), job_uuid,))
    finally:
        try:
            cursor.close()
        except Exception as exception:
            print("Exception closing cursor: ")
            print(exception)
        try:
            conn.close()
        except Exception as exception:
            print("Exception closing conection: ")
            print(exception)


def store_motif(job_uuid, pssm):
    print("storing motif...")
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()

        # did this way rather than using execute's string substitution because I
        # kept getting a TypeError: float argument required, not str:
        sql = """insert into motifs (job_uuid, name, score) values ('%s', '%s', %f);
           select LAST_INSERT_ID();""" % (str(job_uuid), pssm.getName(), float(pssm.getEValue()),)
        print("sql = " + sql)

        cursor.execute(sql)
        row = cursor.fetchone()
        print(row)

        motif_id = row[0]
        print("storing motif:::" + str(motif_id))

        # write pssm matrix
        for scores in pssm.getMatrix():
            print("storing matrix")
            cursor.execute("insert into pssms (motif_id, a, t, c, g) values (%s,%f,%f,%f,%f);",
                (motif_id, float(scores[0]), float(scores[1]), float(scores[2]), float(scores[3]),))
                
        # motif_id int NOT NULL,
        # entrez_gene_id int,
        # sequence,
        # start,
        # quality
                
        # sites is a dictionary w/ keys: gene, start, match, site
        sites = pssm.nsites
        for site in sites:
            print("storing site")
            cursor.execute("insert into sites (motif_id, entrez_gene_id, sequence, start, quality) values (%d, %d, %s, %d, %s)",
                (motif_id, site['gene'], site['site'], site['start'], site['match'],))
        
        print("done storing motif")
        return motif_id

    finally:
        try:
            cursor.close()
        except Exception as exception:
            print("Exception closing cursor: ")
            print(exception)
        try:
            conn.close()
        except Exception as exception:
            print("Exception closing conection: ")
            print(exception)


def store_mirvestigator_scores(motif_id, scores):
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()

        # motif_id int NOT NULL,
        # mirna_name varchar(100),              -- miRNA.name
        # mirna_seed varchar(8),                -- miRNA.seed
        # seedModel varchar(12),                -- model
        # alignment varchar(100),               -- statePath
        # viterbi_p float,                      -- vitPValue

        for score in scores:
            cursor.execute(
                """
                insert into mirvestigator_scores (motif_id, mirna_name, mirna_seed, seedModel, alignment, viterbi_p)
                                          values (%d, %s, %s, %s, %s, %f);
                """,
                (motif_id, score['miRNA.name'], score['miRNA.seed'], score['model'], ";".join(score['statePath']), score['vitPValue'],))

    finally:
        try:
            cursor.close()
        except Exception as exception:
            print("Exception closing cursor: ")
            print(exception)
        try:
            conn.close()
        except Exception as exception:
            print("Exception closing conection: ")
            print(exception)
    