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
        
        cursor.execute("insert into jobs (uuid, created_at, updated_at, status) values ('%s', '%s', '%s', '%s');"
                       % (job['id'], created_at.isoformat(), created_at.isoformat(), 'queued'))
#        for k, v in job.iteritems():
#            if k!='id':
#                cursor.execute("insert into parameters (job_uuid, key, value) (%s, %s, %s)", (job['id'], k, str(v)))
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


def get_job_status(id):
    conn = _get_db_connection()
    try:
        created_at = datetime.datetime.now()
        cursor = conn.cursor()
        cursor.execute("select * from jobs where uuid=%s;", (id,))
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


def update_job_status(job, status):
    conn = _get_db_connection()
    try:
        now = datetime.datetime.now()
        cursor = conn.cursor()
        cursor.execute("update jobs set status='%s', updated_at='%s' where uuid='%s';"
                       % (status, now.isoformat(), job['id'],))
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
