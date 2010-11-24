import Pyro.core
import datetime
import time
import uuid
import MySQLdb
from miRvestigator_job import Job
from multiprocessing import Process, Queue, cpu_count
import mirv_worker


SHUTDOWN_FLAG = -1


def _get_db_connection():
    return MySQLdb.connect("localhost","mirv","mirvestigator","mirvestigator")

def create_job_in_db(job):
    conn = _get_db_connection()
    try:
        created_at = datetime.datetime.now()
        cursor = conn.cursor()
        cursor.execute("insert into jobs (uuid, created_at, updated_at, status) values ('%s', '%s', '%s', '%s');"
                       % (job['id'], created_at.isoformat(), created_at.isoformat(), 'queued'))
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


# wait to take a job from the queue and do it
def start_worker(id, q):
    print("worker %d started" % (id))
    while (True):
        job = q.get()
        if (job==SHUTDOWN_FLAG):
            break
        print("worker %d computing job %s." % (id, job['id']))

        # parse params out of job
        genes = job['genes']
        bgModel = job['bgModel']
        wobble = (job['wobble'] == 'yes')
        cut = float(job['cut'])
        jobName = job['jobName']
        topRet = data['topRet']

        # condense seed models and motif sizes into arrays of ints
        seedModels = [int(job[s]) for s in ['s6','s7','s8'] if s in job and job[s]]
        motifSizes = [int(job[m]) for m in ['m6', 'm8'] if m in job and job[m]]

        mirv_worker.run(genes, seedModels, wobble, cut, bgModel, motifSizes, jobName, topRet=10, eMailAddr='')

        print("worker %d done job %s." % (id, job['id']))
        update_job_status(job, 'done')
    print("worker %d done." % (id))


# Pyro remote object
class TestServer(Pyro.core.ObjBase):

    def __init__(self):
        Pyro.core.ObjBase.__init__(self)

    def setQueue(self, q):
        self.q = q

    def submit_job(self, job):
        id = uuid.uuid1()
        job['id'] = id
        print("Job %s created %s" % (job['id'], job['created'].strftime('%Y.%m.%d %H:%M:%S')))
        create_job_in_db(job)
        # put params in DB
        q.put(job)
        return id



if __name__ == '__main__':
    q = Queue()

    num_workers = 4

    try:
        cores = cpu_count()
        num_workers = cores
    except Exception as e:
        print("can't detect number of cpus")
        print(e)

    # start workers
    workers = []
    for i in range(num_workers):
        p = Process(target=start_worker, args=(i,q,))
        p.start()
        workers.append(p)

    Pyro.core.initServer()
    daemon = Pyro.core.Daemon()
    test_server = TestServer()
    test_server.setQueue(q)
    uri = daemon.connect(test_server, 'miR_server')

    print uri
    uriOut = open('/var/www/uri','w')
    uriOut.write(str(uri))
    uriOut.close()

    daemon.requestLoop()

    for p in workers:
        p.join()
