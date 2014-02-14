<<<<<<< HEAD:inventory_manager/tasks.py
from celery.task import Task
from libs.gdocs import read_doc, rip_doc
from libs.gdoc_config import *
=======
from datetime import timedelta

from celery.task import PeriodicTask
from .libs.gdocs import read_doc, rip_doc
from .libs.godcs_config import *
>>>>>>> dev:apps/inventory_manager/tasks.py


class SyncDbWithTrackerDoc(Task):

    def run(self, *args, **kwargs):
        doc = read_doc(GDOCS_USER, GDOCS_PASSWD, GDOCS_DOCNAME, GDOCS_SHEET)
        rip_doc(doc)


if __name__ == '__main__':
    sync = SyncDbWithTrackerDoc()
    sync.run()