#
# Interact with the mirvestigator MySQL database
#

import MySQLdb
import datetime
import time
import re
import sys

## Note that several of these methods use python's string formatting
## to build SQL strings, which is bad. This was done due to a problem
## with getting cursor.execute("insert into foo values (%s, %f, %d)", (a,b,c))
## to work with either decimal or floating point values.


def log(str):
    sys.stderr.write(str)
    sys.stderr.write("\n")
    sys.stderr.flush()


# a simplistic form of sanitizing input
# drop characters that are special to sql
_sanitize_re = re.compile(r"[\\\"\';]")
def _sanitize(s):
    return _sanitize_re.sub("", s)

def _get_db_connection():
    return MySQLdb.connect("localhost","mirv","mirvestigator","mirvestigator")


def create_job_in_db(job):
    conn = _get_db_connection()
    try:
        created_at = datetime.datetime.now()
        cursor = conn.cursor()

        job_uuid = job['id']
        
        # store entry in jobs table
        cursor.execute("insert into jobs (uuid, created_at, updated_at, status) values ('%s', '%s', '%s', '%s');"
                       % (job_uuid, created_at.isoformat(), created_at.isoformat(), 'queued',))
        
        # store parameters
        for k, v in job.iteritems():
            if k!='id' and k!='genes':
                if k=='jobName':
                    v = _sanitize(v)
                cursor.execute("insert into parameters (job_uuid, name, value) values (%s, %s, %s);",
                               (job_uuid, k, str(v),) )

       #store genes
        if (job['genes']):
            for gene in job['genes']:
                gene = _sanitize(gene)[0:20]
                cursor.execute("insert into genes (job_uuid, name) values ('%s', '%s');" % (job_uuid, gene,) )

    finally:
        try:
            cursor.close()
        except Exception as exception:
            log("Exception closing cursor: \n")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)


def delete_job(job_uuid):
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()

        # delete parameters
        cursor.execute("delete from parameters where job_uuid=%s;", (job_uuid,))

        # delete genes
        cursor.execute("delete from genes where job_uuid=%s;", (job_uuid,))

        # for each motif, delete pssms, sites, and mirvestigator scores
        cursor.execute("select id from motifs where job_uuid=%s;", (job_uuid,))
        result_set = cursor.fetchall()
        for row in result_set:
            cursor.execute("delete from pssms where motif_id=%d", (int(row[0]),))
            cursor.execute("delete from sites where motif_id=%d", (int(row[0]),))
            cursor.execute("delete from mirvestigator_scores where motif_id=%d", (int(row[0]),))

        # delete motifs
        cursor.execute("delete from motifs where job_uuid=%s;", (job_uuid,))

        # delete entry in jobs table
        cursor.execute("delete from jobs where uuid=%s;", (job_uuid,))

    finally:
        try:
            cursor.close()
        except Exception as exception:
            log("Exception closing cursor: \n")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)


# find jobs submitted prior to the cutoff date
# returns a list of job uuids
def find_old_jobs(cutoff_datetime):
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()

        # for each motif, delete pssms, sites, and mirvestigator scores
        cursor.execute("select uuid from jobs where created_at < %s;", (cutoff_datetime.isoformat(),))
        result_set = cursor.fetchall()
        uuids = []
        for row in result_set:
            uuids.append(row[0])

        return uuids
    finally:
        try:
            cursor.close()
        except Exception as exception:
            log("Exception closing cursor: \n")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)


def read_parameters(job_uuid):
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()
        
        # job_name = user defined name
        # job_id = job_id
        # genes_submitted = number of genes submitted
        # annotated_sequences = number of genes with an annotated sequence
        # motif_sizes = an array of the set [6, 7, 8]
        # background_model = Default or 3' UTR
        # model_wobble = yes or no, if yes then tack on the G or U min freq

        cursor.execute("""
            select name, value
            from parameters
            where job_uuid=%s""", (job_uuid,))
        result_set = cursor.fetchall()

        # build a dictionary of parameters
        parameters = {}
        for row in result_set:
            parameters[row[0]] = row[1]

        motif_sizes = []
        if (parameters['m6']):
            motif_sizes.append("6 bp")
        if (parameters['m8']):
            motif_sizes.append("8 bp")
        parameters['motif_sizes'] = motif_sizes

        seed_model = []
        if (parameters['s6']):
            seed_model.append("6mer")
        if (parameters['s7']):
            seed_model.append("7mer")
        if (parameters['s8']):
            seed_model.append("8mer")
        parameters['seed_model'] = seed_model

        if (parameters['wobble']=='yes'):
            parameters['model_wobble'] = 'Yes (' + parameters['cut'] + ')'
        else:
            parameters['model_wobble'] = 'No'

        cursor.execute("""
            select name, sequence
            from genes
            where job_uuid=%s""", (job_uuid,))
        result_set = cursor.fetchall()
        genes = 0
        annotated_sequences = 0
        for row in result_set:
            genes += 1
            if (row[1]==1):
                annotated_sequences += 1

        parameters['genes_submitted'] = genes
        parameters['annotated_sequences'] = annotated_sequences

        return parameters

    finally:
        try:
            cursor.close()
        except Exception as exception:
            log("Exception closing cursor: ")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)
    

def get_job_status(job_uuid):
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("select * from jobs where uuid=%s;", (job_uuid,))
        row = cursor.fetchone()
        result = {}
        if (row==None):
            result['created_at'] = '???';
            result['updated_at'] = '???';
            result['status'] = "not found";
        else:
            result['created_at'] = row[1].strftime('%Y.%m.%d %H:%M:%S');
            result['updated_at'] = row[2].strftime('%Y.%m.%d %H:%M:%S');
            result['status'] = row[3];
        return result
    finally:
        try:
            cursor.close()
        except Exception as exception:
            log("Exception closing cursor: ")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)


def update_job_status(job_uuid, status, message=None):
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
            log("Exception closing cursor: ")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)


def store_genes(job_uuid, genes):
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()

        #store genes
        if (genes):
            for gene in genes:
                gene = _sanitize(gene)[0:20]
                cursor.execute("insert into genes (job_uuid, name) values ('%s', '%s');" %
                               (job_uuid, gene,) )
    finally:
        try:
            cursor.close()
        except Exception as exception:
            log("Exception closing cursor: ")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)


def set_genes_annotated(job_uuid, sequence_dict):
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()

        #update genes to indicate whether sequence was found
        if (sequence_dict):
            for gene in sequence_dict.keys():
                gene = _sanitize(gene)[0:20]
                cursor.execute("update genes set sequence=true where job_uuid='%s' and name='%s';" %
                               (job_uuid, gene,) )
    finally:
        try:
            cursor.close()
        except Exception as exception:
            log("Exception closing cursor: ")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)


def store_motif(job_uuid, pssm):
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()

        # did this way rather than using execute's string substitution because I
        # kept getting a TypeError: float argument required, not str:
        sql = """
            insert into motifs
            (job_uuid, name, score)
            values ('%s', '%s', %f);""" % (str(job_uuid), pssm.getName(), float(pssm.getEValue()),)

        cursor.execute(sql)
        motif_id = cursor.lastrowid

        # write pssm matrix
        for scores in pssm.getMatrix():
            sql = """
                insert into pssms
                (motif_id, a, t, c, g)
                values ('%s',%f,%f,%f,%f);""" % (motif_id, float(scores[0]), float(scores[1]), float(scores[2]), float(scores[3]),)
            cursor.execute(sql)
                
        # motif_id int NOT NULL,
        # entrez_gene_id int,
        # sequence,
        # start,
        # quality
                
        # sites is a dictionary w/ keys: gene, start, match, site
        sites = pssm.nsites
        for site in sites:
            cursor.execute("""
                insert into sites
                (motif_id, entrez_gene_id, sequence, start, quality)
                values (%d, '%s', '%s', %d, '%s')""" %
                (motif_id, str(site['gene']), site['site'], int(site['start']), site['match'],))
        
        return motif_id

    finally:
        try:
            cursor.close()
        except Exception as exception:
            log("Exception closing cursor: ")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)


def read_motifs(job_uuid):
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()

        # read motifs for this job
        cursor.execute("""
            select id, job_uuid, name, score
            from motifs
            where job_uuid = %s;""",
            (str(job_uuid),))
        result_set = cursor.fetchall()
        motifs = []
        for row in result_set:
            motif = {}
            motif['motif_id'] = int(row[0])
            motif['job_uuid'] = row[1]
            motif['name'] = row[2]
            motif['score'] = float(row[3])
            motifs.append(motif)

        # read pssm matrix
        for motif in motifs:
            cursor.execute("""
                select a, t, c, g
                from pssms
                where motif_id=%d;""" %
                (motif['motif_id'],))
            result_set = cursor.fetchall()
            matrix = []
            for row in result_set:
                matrix.append([row[0], row[1], row[2], row[3]])
            motif['matrix'] = matrix

        # read sites
        # each site is a dictionary w/ keys: gene, start, match, site
        for motif in motifs:
            cursor.execute("""
                select entrez_gene_id, sequence, start, quality
                from sites
                where motif_id=%d;""" %
                (motif['motif_id'],))
            result_set = cursor.fetchall()
            sites = []
            for row in result_set:
                site = {}
                site['gene']  = row[0]
                site['site']  = row[1]
                site['start'] = row[2]
                site['match'] = row[3]
                sites.append(site)
            motif['sites'] = sites

        return motifs

        # construct a list of pssm objects
        # pssms = []
        # for motif in motifs:
        #     #pssm(self, pssmFileName=None, biclusterName=None, nsites=None, eValue=None, pssm=None, genes=None)
        #     pssms.append(pssm(  biclusterName=motif['name'],
        #                         nsites=motif['sites'],
        #                         eValue=motif['score'],
        #                         pssm=motif['matrix']))
        # return pssms

    finally:
        try:
            cursor.close()
        except Exception as exception:
            log("Exception closing cursor: ")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)


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
                                          values (%d, '%s', '%s', '%s', '%s', %f);
                """ %
                (motif_id, score['miRNA.name'], score['miRNA.seed'], score['model'], ";".join(score['statePath']), score['vitPValue'],))
    finally:
        try:
            cursor.close()
        except Exception as exception:
            log("Exception closing cursor: ")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)


def read_mirvestigator_scores(motif_id):
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            select motif_id, mirna_name, mirna_seed, seedModel, alignment, viterbi_p
            from mirvestigator_scores
            where motif_id=%d;
            """ % (int(motif_id),))
        result_set = cursor.fetchall()

        scores = []
        for row in result_set:
            score = {}
            score['miRNA.name'] = row[1]
            score['miRNA.seed'] = row[2]
            score['model'] = row[3]
            score['statePath'] = row[4].split(";")
            score['vitPValue'] = row[5]
            scores.append(score)

        return scores

    finally:
        try:
            cursor.close()
        except Exception as exception:
            log("Exception closing cursor: ")
            log(exception)
        try:
            conn.close()
        except Exception as exception:
            log("Exception closing conection: ")
            log(exception)
    