import Pyro.core
import datetime
import time
import uuid
import traceback

from mirv_db import create_job_in_db, update_job_status
from multiprocessing import Process, Queue, cpu_count
import mirv_worker
import admin_emailer



QUEUE_WARN_SIZE = 100
SHUTDOWN_FLAG = -1



adminEmailer = admin_emailer.AdminEmailer()

error_msg_template = """
Exception in mirv_worker %d on job %s.

Stacktrace:
%s
%s
"""


# wait to take a job from the queue and do it
def start_worker(id, q):
    print("worker %d started" % (id))
    while (True):
        job = q.get()
        if (job==SHUTDOWN_FLAG):
            break
        update_job_status(job['id'], "started on worker %d" % (id))
        print("worker %d computing job %s." % (id, job['id']))

        # parse params out of job
        genes = job['genes']
        bgModel = job['bgModel']
        wobble = (job['wobble'] == 'yes')
        cut = float(job['cut'])
        jobName = job['jobName']
        topRet = job['topRet']
        notify_mail = job['notify_mail']

        # condense seed models and motif sizes into arrays of ints
        seedModels = [int(job[s]) for s in ['s6','s7','s8'] if s in job and job[s]]
        motifSizes = [int(job[m]) for m in ['m6', 'm8'] if m in job and job[m]]

        try:
            mirv_worker.run(job['id'], genes, seedModels, wobble, cut, bgModel, motifSizes, jobName, topRet)
            print("worker %d done job %s." % (id, job['id']))
            update_job_status(job['id'], 'done')
            if (notify_mail):
                adminEmailer.notify_complete( notify_mail.split(","), str(job['id']), jobName )
        except Exception as e:
            print("Exception in mirv_worker %d on job %s." %  (id, str(job['id'])))
            traceback.print_stack()
            traceback.print_exc()
            try:
                update_job_status(job['id'], 'error')
            except Exception as e2:
                print(e)
        try:
            adminEmailer.warn(error_msg_template %  (id, str(job['id']), traceback.format_stack(), traceback.format_exc(),))
        except Exception as e2:
            print(e)
        try:
            adminEmailer.notify_error(error_msg_template %  (id, str(job['id']), traceback.format_stack(), traceback.format_exc(),))
        except Exception as e2:
            print(e)

    print("worker %d exiting." % (id))


# Pyro remote object
class MiRvestigatorServer(Pyro.core.ObjBase):

    def __init__(self):
        Pyro.core.ObjBase.__init__(self)

    def setQueue(self, q):
        self.q = q

    def submit_job(self, job):
        id = uuid.uuid1()
        job['id'] = id
        print("Job %s created %s" % (job['id'], job['created'].strftime('%Y.%m.%d %H:%M:%S')))
        create_job_in_db(job)

        # put job in queue
        try:
            q.put(job, block=false)
        except Queue.Full as e:
            traceback.print_stack()
            traceback.print_exc()
            update_job_status(job['id'], "error")
            return

        # update status to queued
        try:
            q_len = q.qsize()
            if (q_len >= QUEUE_WARN_SIZE):
                adminEmailer.warn("Queue is getting too long. There are currently %d items in the queue." % q_len)
            update_job_status(job['id'], "queued", "queue length %d" % q_len)
        except NotImplementedError:
            print("q.qsize not supported")
            update_job_status(job['id'], "queued")
        return id



if __name__ == '__main__':
    q = Queue(200)

    num_workers = 4

    try:
        cores = cpu_count()
        num_workers = cores
    except Exception as e:
        print("can't detect number of cpus")
        print(e)

    # start worker child processes
    workers = []
    for i in range(num_workers):
        p = Process(target=start_worker, args=(i,q,))
        p.start()
        workers.append(p)

    Pyro.core.initServer()
    daemon = Pyro.core.Daemon()
    test_server = MiRvestigatorServer()
    test_server.setQueue(q)
    uri = daemon.connect(test_server, 'miR_server')

    print uri
    uriOut = open('/var/www/uri','w')
    uriOut.write(str(uri))
    uriOut.close()

    daemon.requestLoop()

    for p in workers:
        p.join()
