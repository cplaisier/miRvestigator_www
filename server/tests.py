import datetime
import mirv_db


if __name__ == '__main__':
    old = datetime.datetime.now()
    uuids = mirv_db.find_old_jobs(old)
    for uuid in uuids:
        mirv_db.delete_job(uuid)
