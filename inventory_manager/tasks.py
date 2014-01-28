from celery.task import Task

from gdocs import read_doc, rip_doc
from gdoc_config import *


class SyncDbWithTrackerDoc(Task):

    def run(self, *args, **kwargs):
        doc = read_doc(GDOCS_USER, GDOCS_PASSWD, GDOCS_DOCNAME, GDOCS_SHEET)
        rip_doc(doc, API_LIST_URI, API_DETAIL_URI, API_KEY)


class TestSpam(Task):
    def run(self, *args, **kwargs):
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login('v.forgione@gmail.com', '7h3M0n@R(h')
        server.sendmail('v.forgione@gmail.com', 'vince@doggyloot.com', 'this has been a test')
        server.quit()


if __name__ == '__main__':
    sync = SyncDbWithTrackerDoc()
    sync.run()
