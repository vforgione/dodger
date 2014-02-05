from datetime import timedelta

from celery.task import PeriodicTask
from .libs.gdocs import read_doc, rip_doc
from .libs.godcs_config import *


class SyncDbWithTrackerDoc(PeriodicTask):

    run_every = timedelta(hours=1)

    def run(self, *args, **kwargs):
        doc = read_doc(GDOCS_USER, GDOCS_PASSWD, GDOCS_DOCNAME, GDOCS_SHEET)
        rip_doc(doc, API_LIST_URI, API_DETAIL_URI, API_KEY)


if __name__ == '__main__':
    sync = SyncDbWithTrackerDoc()
    sync.run()
