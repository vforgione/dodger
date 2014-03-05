import os

manage = os.path.abspath(
    os.path.join(os.curdir, '..', '..', 'manage.py')
)

print manage

for filename in os.listdir(os.path.abspath(os.curdir)):
    if filename.endswith('.json'):
        os.system("python %s loaddata %s" % (manage, os.path.abspath(filename)))
