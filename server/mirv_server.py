#################################################################
# @Program: miRvestigator                                       #
# @Version: 2                                                   #
# @Author: Chris Plaisier                                       #
# @Author: Christopher Bare                                     #
# @Sponsored by:                                                #
# Nitin Baliga, ISB                                             #
# Institute for Systems Biology                                 #
# 1441 North 34th Street                                        #
# Seattle, Washington  98103-8904                               #
# (216) 732-2139                                                #
# @Also Sponsored by:                                           #
# Luxembourg Systems Biology Grant                              #
#                                                               #
# If this program is used in your analysis please mention who   #
# built it. Thanks. :-)                                         #
#                                                               #
# Copyright (C) 2010 by Institute for Systems Biology,          #
# Seattle, Washington, USA.  All rights reserved.               #
#                                                               #
# This source code is distributed under the GNU Lesser          #
# General Public License, the text of which is available at:    #
#   http://www.gnu.org/copyleft/lesser.html                     #
#################################################################

import Pyro.core
import datetime
import time
import uuid
import traceback
from Queue import Full

from mirv_db import create_job_in_db, update_job_status, get_species_by_mirbase_id, get_unfinished_jobs
from multiprocessing import Process, Queue, cpu_count
import mirv_worker
import admin_emailer
import conf




QUEUE_WARN_SIZE = 100
QUEUE_MAX_SIZE = 200
SHUTDOWN_FLAG = -1



adminEmailer = admin_emailer.AdminEmailer()

error_msg_template = """
Exception in mirv_worker %d on job %s.

Stacktrace:
%s

Exception:
%s
"""


def delete_old_jobs(cutoff_datetime):
    pass


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
        print job
        genes = job['genes']
        geneId = job['geneId']
        wobble = (job['wobble'] == 'yes')
        cut = float(job['cut'])
        jobName = job['jobName']
        topRet = job['topRet']
        mirbase_species = job['species']
        notify_mail = job['notify_mail']
        bgModel = job['bgModel']
        if job['viral']=='True':
            viral = True
        else:
            viral = False

        # condense seed models and motif sizes into arrays of ints
        seedModels = [int(job[s]) for s in ['s6','s7','s8'] if s in job and job[s]]
        motifSizes = [int(job[m]) for m in ['m6', 'm8'] if m in job and job[m]]

        try:
            # run the job
            r = mirv_worker.run(job['id'], genes, geneId, seedModels, wobble, cut, motifSizes, jobName, mirbase_species, bgModel, topRet, viral)

            # notify on success
            if r:
                print("worker %d finished job %s." % (id, job['id']))
                if (notify_mail):
                    adminEmailer.notify_complete( notify_mail.split(","), str(job['id']), jobName )
            else:
                print("worker %d, job %s failed." % (id, job['id']))

        except Exception as e:
            print("Exception in mirv_worker %d on job %s." %  (id, str(job['id'])))
            traceback.print_stack()
            traceback.print_exc()
            try:
                update_job_status(job['id'], 'error')
            except Exception as e2:
                traceback.print_stack()
                traceback.print_exc()
            try:
                adminEmailer.warn(error_msg_template %  (id, str(job['id']), traceback.format_stack(), traceback.format_exc(),))
            except Exception as e2:
                traceback.print_stack()
                traceback.print_exc()
            try:
                if (notify_mail):
                    #recipients, job_uuid, job_name
                    adminEmailer.notify_error(notify_mail.split(","), str(job['id']), jobName)
            except Exception as e2:
                traceback.print_stack()
                traceback.print_exc()

    print("worker %d exiting." % (id))


# Pyro remote object
class MiRvestigatorServer(Pyro.core.ObjBase):

    def __init__(self):
        Pyro.core.ObjBase.__init__(self)

    def setQueue(self, q):
        self.q = q

    def pickup_unfinished(self):
        print "continuing unfinished jobs..."
        for uuid, job in get_unfinished_jobs().items():
            job['id'] = uuid
            self.q.put(job, block=False)
        print "unfinished jobs queued"

    def submit_job(self, job):
        id = uuid.uuid1()
        job['id'] = id
        print("Job %s created %s" % (job['id'], job['created'].strftime('%Y.%m.%d %H:%M:%S')))
        create_job_in_db(job)

        # put job in queue
        try:
            q.put(job, block=False)
        except Full as e:
            traceback.print_stack()
            traceback.print_exc()
            update_job_status(job['id'], "error")
            raise

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
    q = Queue(QUEUE_MAX_SIZE)

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
    test_server.pickup_unfinished()
    uri = daemon.connect(test_server, 'miR_server')

    print uri
    uriOut = open(conf.tmp_dir+'/uri','w')
    uriOut.write(str(uri))
    uriOut.close()

    daemon.requestLoop()

    for p in workers:
        p.join()
