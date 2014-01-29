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

### celery settings

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

`~/dodger-env/dodger/uwsgi.ini`

```
[uwsgi]

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

### uwsgi startup

`/etc/init.d/uwsgi`

```
#!/bin/sh

### BEGIN INIT INFO
# Provides: uwsgi
# Required-Start: $all
# Required-Stop: $all
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: starts the uwsgi app server
# Description: starts uwsgi app server using start-stop-daemon
### END INIT INFO

DAEMON=/usr/local/bin/uwsgi

OWNER=deploy

NAME=uwsgi
DESC=uwsgi

test -x $DAEMON || exit 0

set -e

DAEMON_OPTS="--ini /home/deploy/dodger-env/dodger/uwsgi.ini"

case "$1" in
    start)
        echo -n "Starting $DESC: "
        start-stop-daemon --start --chuid $OWNER:$OWNER --user $OWNER \
        --exec $DAEMON -- $DAEMON_OPTS
        echo "$NAME."
    ;;
    stop)
        echo -n "Stopping $DESC: "
        start-stop-daemon --signal 3 --user $OWNER --quiet --retry 2 --stop \
        --exec $DAEMON
        echo "$NAME."
    ;;
    reload)
        killall -1 $DAEMON
    ;;
    force-reload)
        killall -15 $DAEMON
    ;;
    restart)
        echo -n "Restarting $DESC: "
        start-stop-daemon --signal 3 --user $OWNER --quiet --retry 2 --stop \
        --exec $DAEMON
        sleep 1
        start-stop-daemon --user $OWNER --start --quiet --chuid $OWNER:$OWNER \
        --exec $DAEMON -- $DAEMON_OPTS
        echo "$NAME."
    ;;
    status)
        killall -10 $DAEMON
    ;;
    *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|reload|force-reload|status}" >&2
        exit 1
    ;;
esac

exit 0

```

### nginx

`/etc/nginx/nginx.conf`

```

```

### celery startup

`/etc/init.d/celeryd`

```
#!/bin/sh -e
### BEGIN INIT INFO
# Provides:          celeryd
# Required-Start:    $network $local_fs $remote_fs
# Required-Stop:     $network $local_fs $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: celery task worker daemon
### END INIT INFO

# ============================================
#  celeryd - Starts the Celery worker daemon.
# ============================================
#
# :Usage: /etc/init.d/celeryd {start|stop|force-reload|restart|try-restart|status}
# :Configuration file: /etc/default/celeryd
#
# See http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html#generic-init-scripts


# some commands work asyncronously, so we'll wait this many seconds
SLEEP_SECONDS=5

DEFAULT_PID_FILE="/var/run/celery/%n.pid"
DEFAULT_LOG_FILE="/var/log/celery/%n.log"
DEFAULT_LOG_LEVEL="INFO"
DEFAULT_NODES="celery"
DEFAULT_CELERYD="-m celery.bin.celeryd_detach"

CELERY_DEFAULTS=${CELERY_DEFAULTS:-"/etc/default/celeryd"}

test -f "$CELERY_DEFAULTS" && . "$CELERY_DEFAULTS"

# Set CELERY_CREATE_DIRS to always create log/pid dirs.
CELERY_CREATE_DIRS=${CELERY_CREATE_DIRS:-1}
CELERY_CREATE_RUNDIR=$CELERY_CREATE_DIRS
CELERY_CREATE_LOGDIR=$CELERY_CREATE_DIRS
if [ -z "$CELERYD_PID_FILE" ]; then
    CELERYD_PID_FILE="$DEFAULT_PID_FILE"
    CELERY_CREATE_RUNDIR=1
fi
if [ -z "$CELERYD_LOG_FILE" ]; then
    CELERYD_LOG_FILE="$DEFAULT_LOG_FILE"
    CELERY_CREATE_LOGDIR=1
fi

CELERYD_LOG_LEVEL=${CELERYD_LOG_LEVEL:-${CELERYD_LOGLEVEL:-$DEFAULT_LOG_LEVEL}}
CELERYD_MULTI=${CELERYD_MULTI:-"celeryd-multi"}
CELERYD=${CELERYD:-$DEFAULT_CELERYD}
CELERYD_NODES=${CELERYD_NODES:-$DEFAULT_NODES}

export CELERY_LOADER

if [ -n "$2" ]; then
    CELERYD_OPTS="$CELERYD_OPTS $2"
fi

CELERYD_LOG_DIR=`dirname $CELERYD_LOG_FILE`
CELERYD_PID_DIR=`dirname $CELERYD_PID_FILE`

# Extra start-stop-daemon options, like user/group.
SUDOCMD=""
if [ -n "$CELERYD_USER" ]; then
    #DAEMON_OPTS="$DAEMON_OPTS --uid=$CELERYD_USER"
    SUDOCMD="sudo -u $CELERYD_USER "
    CELERYD_MULTI="$SUDOCMD $CELERYD_MULTI"
fi
if [ -n "$CELERYD_GROUP" ]; then
    DAEMON_OPTS="$DAEMON_OPTS --gid=$CELERYD_GROUP"
fi

if [ -n "$CELERYD_CHDIR" ]; then
    DAEMON_OPTS="$DAEMON_OPTS --workdir=$CELERYD_CHDIR"
fi


check_dev_null() {
    if [ ! -c /dev/null ]; then
        echo "/dev/null is not a character device!"
        exit 75  # EX_TEMPFAIL
    fi
}


maybe_die() {
    if [ $? -ne 0 ]; then
        echo "Exiting: $* (errno $?)"
        exit 77  # EX_NOPERM
    fi
}

create_default_dir() {
    if [ ! -d "$1" ]; then
        echo "- Creating default directory: '$1'"
        mkdir -p "$1"
        maybe_die "Couldn't create directory $1"
        echo "- Changing permissions of '$1' to 02755"
        chmod 02755 "$1"
        maybe_die "Couldn't change permissions for $1"
        if [ -n "$CELERYD_USER" ]; then
            echo "- Changing owner of '$1' to '$CELERYD_USER'"
            chown "$CELERYD_USER" "$1"
            maybe_die "Couldn't change owner of $1"
        fi
        if [ -n "$CELERYD_GROUP" ]; then
            echo "- Changing group of '$1' to '$CELERYD_GROUP'"
            chgrp "$CELERYD_GROUP" "$1"
            maybe_die "Couldn't change group of $1"
        fi
    fi
}


check_paths() {
    if [ $CELERY_CREATE_LOGDIR -eq 1 ]; then
        create_default_dir "$CELERYD_LOG_DIR"
    fi
    if [ $CELERY_CREATE_RUNDIR -eq 1 ]; then
        create_default_dir "$CELERYD_PID_DIR"
    fi
}

create_paths() {
    create_default_dir "$CELERYD_LOG_DIR"
    create_default_dir "$CELERYD_PID_DIR"
}

export PATH="${PATH:+$PATH:}/usr/sbin:/sbin"


_get_pid_files() {
    [ ! -d "$CELERYD_PID_DIR" ] && return
    echo `ls -1 "$CELERYD_PID_DIR"/*.pid 2> /dev/null`
}

stop_workers () {
    $CELERYD_MULTI stopwait $CELERYD_NODES --pidfile="$CELERYD_PID_FILE"
    sleep $SLEEP_SECONDS
}


start_workers () {
    $CELERYD_MULTI start $CELERYD_NODES $DAEMON_OPTS        \
                         --pidfile="$CELERYD_PID_FILE"      \
                         --logfile="$CELERYD_LOG_FILE"      \
                         --loglevel="$CELERYD_LOG_LEVEL"    \
                         --cmd="$CELERYD"                   \
                         $CELERYD_OPTS &
    sleep $SLEEP_SECONDS
}


restart_workers () {
    $CELERYD_MULTI restart $CELERYD_NODES $DAEMON_OPTS      \
                           --pidfile="$CELERYD_PID_FILE"    \
                           --logfile="$CELERYD_LOG_FILE"    \
                           --loglevel="$CELERYD_LOG_LEVEL"  \
                           --cmd="$CELERYD"                 \
                           $CELERYD_OPTS &
    sleep $SLEEP_SECONDS
}

check_status () {
    local pid_files=
    pid_files=`_get_pid_files`
    [ -z "$pid_files" ] && echo "celeryd not running (no pidfile)" && exit 1

    local one_failed=
    for pid_file in $pid_files; do
        local node=`basename "$pid_file" .pid`
        local pid=`cat "$pid_file"`
        local cleaned_pid=`echo "$pid" | sed -e 's/[^0-9]//g'`
        if [ -z "$pid" ] || [ "$cleaned_pid" != "$pid" ]; then
            echo "bad pid file ($pid_file)"
        else
            local failed=
            kill -0 $pid 2> /dev/null || failed=true
            if [ "$failed" ]; then
                echo "celeryd (node $node) (pid $pid) is stopped, but pid file exists!"
                one_failed=true
            else
                echo "celeryd (node $node) (pid $pid) is running..."
            fi
        fi
    done

    [ "$one_failed" ] && exit 1 || exit 0
}


case "$1" in
    start)
        check_dev_null
        check_paths
        start_workers
    ;;

    stop)
        check_dev_null
        check_paths
        stop_workers
    ;;

    reload|force-reload)
        echo "Use restart"
    ;;

    status)
        check_status
    ;;

    restart)
        check_dev_null
        check_paths
        restart_workers
    ;;
    try-restart)
        check_dev_null
        check_paths
        restart_workers
    ;;
    create-paths)
        check_dev_null
        create_paths
    ;;
    check-paths)
        check_dev_null
        check_paths
    ;;
    *)
        echo "Usage: /etc/init.d/celeryd {start|stop|restart|kill|create-paths}"
        exit 64  # EX_USAGE
    ;;
esac

exit 0
```

### celery startup defaults

`/etc/defualt/celeryd`

```
# Name of nodes to start
# here we have a single node
CELERYD_NODES="w1"

ENV_MY="/home/deploy/dodger-env"
CELERYD="$ENV_MY/bin/celeryd"
CELERYD_MULTI="$ENV_MY/bin/celeryd-multi"
CELERYCTL="$ENV_MY/bin/celeryctl"

# Where to chdir at start.
CELERYD_CHDIR="$ENV_MY/dodger/"
ENV_PYTHON="$ENV_MY/bin/python"
# Extra arguments to celeryd
CELERYD_OPTS="-B --loglevel=INFO --events --autoreload"


# %n will be replaced with the nodename.
CELERYD_LOG_FILE="/var/log/celery/%n.log"
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERY_CREATE_RUNDIR=0
CELERY_CREATE_LOGDIR=0

# Workers should run as an unprivileged user.
CELERYD_USER="deploy"
```

