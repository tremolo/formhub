# Installation Guide

*This document describes how to install and run formhub as a dedicated server image. If you wish to run it on a shared computer, the use of a virtualized environment, such as [VirtualBox](https://www.virtualbox.org/) is recommended. Using either [debian](http://www.debian.org/) or [ubuntu](http://www.ubuntu.com/) for the operating system (OS) is recommended. If you choose a different server OS, you will need to replace the [apt-get](https://help.ubuntu.com/community/AptGet/Howto) command with the one corresponding to your system's package manager.*

## *Required Steps*

## 1. Basic System Libraries and Packages

Install using a terminal or command line prompt as the [root](https://wiki.debian.org/Root) user in debian or with the [sudo](https://help.ubuntu.com/community/RootSudo) command in ubuntu:

```
$ sudo apt-get update; sudo apt-get upgrade -y
$ sudo apt-get install -y git build-essential python-all-dev \
  python-pip python-lxml python-magic python-imaging default-jre \
  libjpeg-dev libfreetype6-dev zlib1g-dev rabbitmq-server libxslt1-dev
```

## 2. Define the formhub user account 

Create <tt>fhuser</tt>, the user account which will own and run the formhub processes, and set its password:

```
$ sudo adduser fhuser
$ sudo passwd fhuser
```

## 3. Install [mongoDB](http://mongodb.org/)

According to the mongoDB installation instructions for [debian](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-debian/) and [ubuntu](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/).

Import the public key:

```
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
```

Next, for debian:

```
$ echo 'deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
```

Or ubuntu:
```
$ echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
```

Then finally for either system:
```
$ sudo apt-get update
$ sudo apt-get install mongodb-org 
```

*As of this writing the <tt>apt-get install mongodb-org</tt> command on debian results in a 404 / not found error (the files for version 2.6.1 files are not present in http://downloads-distro.mongodb.org/repo/debian-sysvinit for whatever reason), so you may need to specify the prior stable version like this:*

```
$ sudo apt-get install mongodb-org=2.6.0 mongodb-org-server=2.6.0 mongodb-org-shell=2.6.0 mongodb-org-mongos=2.6.0 mongodb-org-tools=2.6.0
```

## 4. Install [PostgreSQL](http://www.postgresql.org/)

*Prior versions of formhub used [MySQL](https://www.mysql.com/), and while it is technically possible to use it instead, PostgreSQL is strongly recommended. Using PostgreSQL from the start will also make following the future [technical roadmap](../roadmap/README.md) simpler.*

Install the required packages and libraries:

```
$ sudo apt-get install -y postgresql python-psycopg2 postgresql-contrib
$ sudo pip install south
```

Then configure the database for formhub. Create a data folder for the database to use:

```
$ sudo /etc/init.d/postgresql stop
$ sudo mkdir -p /opt/data/formhub/pgsql
$ cd /opt/data/formhub
$ sudo chown postgres pgsql
```

Next, update the configuration file to use it, saving the original version of the <tt>postgresql.conf</tt> in <tt>/etc/postgresql/9.1/main</tt> before making any edits:

```
$ cd /etc/postgresql/9.1/main
$ sudo cp -ip postgresql.conf postgresql.conf.org
```

Change the <tt>data_directory</tt> variable to point to the pgsql formhub data folder (i.e., <tt>/opt/data/formhub/pgsql</tt>).

Unless you already have a valid [SSL certificate]() installed, turn off the <tt>ssl</tt> option:

```
$ sudo vi postgresql.conf
# (edit lines 41 and 80 -- here is the before and after) 
$ diff postgresql.conf.org postgresql.conf
41c41
< data_directory = '/var/lib/postgresql/9.1/main'		# use data in another directory
---
> data_directory = '/opt/data/formhub/pgsql'
80c80
< ssl = true				# (change requires restart)
---
> ssl = false				# (change requires restart)
```
Switch to the <tt>postgres</tt> account and initialize the database and database user for access by the formhub [django](https://www.djangoproject.com/) application.

```
$ sudo su - postgres 
$ /usr/lib/postgresql/9.1/bin/initdb -D /opt/data/formhub/pgsql
$ /usr/lib/postgresql/9.1/bin/pg_ctl -D /opt/data/formhub/pgsql -l logfile start
$ /usr/lib/postgresql/9.1/bin/createuser -P formhubDjangoApp
```

Enter a password for the <tt>formhubDjangoApp</tt> database user. You will need this later, in the django <tt>settings.py</tt> configuration file.

Say no (<tt>n</tt>) to the next series of permission questions:

```
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n
```

Create the logical database <tt>FormhubDjangoDB</tt> for the formhub django application and enable uuid creation:

```
$ /usr/lib/postgresql/9.1/bin/createdb FormhubDjangoDB
$ /usr/lib/postgresql/9.1/bin/psql -d FormhubDjangoDB
```

You will be presented with the <tt>FormhubDjangoDB=#</tt> prompt. Enter the following command, then <tt>\q</tt> to exit the database shell:

```
FormhubDjangoDB=# CREATE EXTENSION "uuid-ossp";
FormhubDjangoDB=# \q
```

Finally, turn postgres off, and exit the postgres account:

```
$ /usr/lib/postgresql/9.1/bin/pg_ctl -D /opt/data/formhub/pgsql -l logfile stop
$ exit
```
Continue as the root or sudo user to edit the [pg_hba.conf](http://www.postgresql.org/docs/9.3/static/auth-pg-hba-conf.html) file for database access security.

As always, copy the existing configuration file first, before making any edits, then change line 90 from <tt>peer</tt> to <tt>md5</tt> (for more about these options, see the [pg_hba.conf](http://www.postgresql.org/docs/9.3/static/auth-pg-hba-conf.html) file docs): 

```
$ cd /etc/postgresql/9.1/main
$ sudo cp -ip pg_hba.conf pg_hba.conf.org
$ sudo vi pg_hba.conf
# (here is the before and after)
$ diff pg_hba.conf.org pg_hba.conf
90c90
< local   all             all                                     peer
---
> local   all             all                                     md5
```

Restart the database, and test that it asks for a password for access:

```
$ sudo /etc/init.d/postgresql restart
$ /usr/lib/postgresql/9.1/bin/psql -d FormhubDjangoDB -U formhubDjangoApp -h localhost
```

If your configurations are correct, you should be prompted for a password, like this:

```
Password for user formhubDjangoApp: 
```

You can either input the password you used to create the <tt>formhubDjangoApp</tt> user earlier, the <tt>\q</tt> to exit, or just <tt>Control-C</tt> to quit.

*Phew!* That was a lot of work, but your databases are ready, and you won't have to touch these settings again, even if you have to reboot or restart the server later.

## 5. Install the formhub repository as user <tt>fhuser</tt>

Switch to the <tt>fhuser</tt> account and make sure you are in the home folder of the correct account:

```
$ sudo su - fhuser
$ pwd
$ whoami
```

You should see <tt>/home/fhuser</tt> as the result of the <tt>pwd</tt> command, and <tt>fhuser</tt> as the result of <tt>whoami</tt>. 

Next, obtain the [formhub source](https://github.com/SEL-Columbia/formhub.git) from [github](https://github.com/):

```
$ git clone https://github.com/SEL-Columbia/formhub.git
```


