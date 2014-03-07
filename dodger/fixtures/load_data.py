import os

manage = os.path.abspath(
    os.path.join(os.curdir, '..', '..', 'manage.py')
)

for filename in os.listdir(os.path.abspath(os.curdir)):
    if filename.endswith('.json'):
        print filename
        os.system("python %s loaddata %s" % (manage, os.path.abspath(filename)))
