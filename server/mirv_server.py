import Pyro.core
import datetime
import time
import uuid

from mirv_db import create_job_in_db, update_job_status
from multiprocessing import Process, Queue, cpu_count
import mirv_worker


SHUTDOWN_FLAG = -1




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

        # condense seed models and motif sizes into arrays of ints
        seedModels = [int(job[s]) for s in ['s6','s7','s8'] if s in job and job[s]]
        motifSizes = [int(job[m]) for m in ['m6', 'm8'] if m in job and job[m]]

        mirv_worker.run(job['id'], genes, seedModels, wobble, cut, bgModel, motifSizes, jobName, topRet)
        # try:
        # except Exception as e:
        #     try:
        #         print("Exception in mirv_worker.run on job " + str(job_uuid))
        #         print(e)
        #         update_job_status(job_uuid, "error")
        #     except Exception as e2:
        #         pass

        print("worker %d done job %s." % (id, job['id']))
        update_job_status(job['id'], 'done')
    print("worker %d done." % (id))


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
        # put params in DB
        q.put(job)
        update_job_status(job['id'], 'queued')
        return id



if __name__ == '__main__':
    q = Queue()

    num_workers = 4

    try:
        cores = cpu_count()
        num_workers = cores * 2
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
