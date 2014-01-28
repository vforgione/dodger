from celery.task import Task

from gdocs import read_doc, rip_doc
from gdoc_config import *


class SyncDbWithTrackerDoc(Task):

    def run(self, *args, **kwargs):
        doc = read_doc(GDOCS_USER, GDOCS_PASSWD, GDOCS_DOCNAME, GDOCS_SHEET)
        rip_doc(doc, API_LIST_URI, API_DETAIL_URI, API_KEY)


if __name__ == '__main__':
    sync = SyncDbWithTrackerDoc()
    sync.run()
