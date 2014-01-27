# dodger debian install


## getting secure

### set hostname

set the hostname to `dodger`

```
root@23.239.4.166:~# hostname
root@23.239.4.166:~# hostname -f
root@23.239.4.166:~# exit
```

### install some stuff

```
root@dodger:~# apt-get install sudo vim
```

### create a new user

```
root@dodger:~# adduser deploy
root@dodger:~# usermod -a -G sudo deploy
```

### add public key for user

```
you@your-laptop:~$ cd ~/.ssh
you@your-laptop:~$ ssh-keygen dodger_deploy__id_rsa
you@your-laptop:~$ scp ~/.ssh/dodger_deploy__id_rsa.pub deploy@dodger:
you@your-laptop:~$ ssh deploy@dodger

deploy@dodger:~$ mkdir ~/.ssh
deploy@dodger:~$ mv dodger_deploy__id_rsa.pub ~/.ssh
deploy@dodger:~$ cd ~/.ssh
deploy@dodger:~$ cat dodger_deploy__id_rsa.pub >> authorized_keys
deploy@dodger:~$ cd
deploy@dodger:~$ chown -R deploy:deploy ~/.ssh
deploy@dodger:~$ chmod 0700 ~/.ssh
deploy@dodger:~$ chmod 0600 ~/.ssh/authorize_keys
```


### disable root login and remove deploy ssh password

```
deploy@dodger:~$ sudo vim /etc/ssh/sshd_config
```

search for line `PasswordAuthentication` and change value to `no`

search for line `PermitRootLogin` and change value to `no`

restart sshd

```
deploy@dodger:~$ sudo service sshd restart
```


### edit local ssh config

```
you@your-laptop:~$ vim ~/.ssh/config
```

append to the file the following

```
Host dodger
    Hostname 23.239.4.166
    User deploy
    IdentityFile ~/.ssh/dodger_deploy__id_rsa
```

and you should be able to log into dodger via `ssh dodger` and run sudo commands.


## installing dodger

### install system packages

#### rabbitmq

```
deploy@dodger:~$ sudo -s

root@dodger:~# wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
root@dodger:~# apt-key add rabbitmq-signing-key-public.asc
root@dodger:~# rm rabbitmq-signing-key-public.asc
root@dodger:~# echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list.d/rabbitmq.list
root@dodger:~# apt-get update
root@dodger:~# apt-get install rabbitmq-server
root@dodger:~# rabbitmq-plugins enable rabbitmq_management
root@dodger:~# rabbitmqctl add_user dodger <password>
root@dodger:~# rabbitmqctl set_permissions -p / dodger ".*" ".*" ".*"
root@dodger:~# service rabbitmq-server restart
```

#### nginx

```
root@dodger:~# apt-get install nginx-full
```

#### postgresql
```
root@dodger:~# apt-get install postgresql postgresql-client libpq-dev
root@dodger:~# su - postgres

postgres@dodger:~$ psql

postgres=# CREATE USER dodger WITH PASSWORD '<password>';
postgres=# CREATE DATABASE dodger OWNER dodger;
postgres=# \q

postgres@dodger:~$ exit

root@dodger:~# vim /etc/postgresql/9.1/main/pg_hba.conf
```

change `local all all peer` to `local all all md5`

```
root@dodger:~# /etc/init.d/postgresql reload
```

#### python and git 

```
deploy@dodger:~$ sudo apt-get install build-essential python-dev python-pip git
```

#### pip installations

```
deploy@dodger:~$ sudo pip install uwsgi virtualenv
deploy@dodger:~$ sudo apt-get install uwsgi-plugin-python
```

### create virtualenv and clone dodger

```
deploy@dodger:~$ virtualenv dodger-env
deploy@dodger:~$ cd dodger-env
deploy@dodger:~$ . bin/activate
(dodger-env)deploy@dodger:~$ git clone https://github.com/doggyloot/dodger.git
(dodger-env)deploy@dodger:~$ pip install -r dodger/requirements.txt
```


## important configs

### celery config

`~/dodger-env/dodger/dodger/settings.py`

```
# import django-celery
import djcelery

# add it to installed apps
INSTALLED_APPS += (
    'djcelery',
    'kombu.transport.django',
)

# import application tasks
djcelery.setup_loader()

# configure celery
BROKER_URL = 'amqp://dodger:<password>@localhost:5672//'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
```

### uwsgi config

`~/dodger-env/dodger/dodger/uwsgi.ini`

```
[uwsgi]

# enable python plugin
plugin = python

# path to project
chdir = /home/deploy/dodger-env/dodger
module = dodger.wsgi

# path to virtualenv
home = /home/deploy/dodger-env

# environment variables
env = DJANGO_SETTINGS_MODULE=dodger.settings

# application configs
master = true
processes = 8
harakiri = 20
max-requests = 100
vacuum = true

# routing
socket = /home/deploy/dodger-env/dodger.sock
chmod-socket = 666

# logging
pidfile = /home/deploy/dodger-env/dodger.pid
daemonize = /home/deploy/dodger-env/uwsgi.log
```

### startup

`/etc/rc.local`

```
uwsgi --ini /home/deploy/dodger-env/dodger/uwsgi.ini

```

### nginx

`/etc/nginx/nginx.conf`

```

```

`/etc/nginx/sites-enabled/dodger`

```

```




























