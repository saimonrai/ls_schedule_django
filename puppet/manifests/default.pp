#!/bin/bash
# Adding shebang just for text highlight in vim

Exec {
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
}

exec { "apt-get update":
  command => "apt-get update",
} 

##### essential packages

package { "tree":
  ensure => present,
}

package { "htop":
  ensure => present,
}

package { "git":
  ensure => present,
}

package { "libpq-dev":
  ensure => present,
}

############################################################
# postgresql
# https://github.com/puppetmodules/puppet-module-postgresql
############################################################

class { "postgresql::server": version => "9.1",
                              listen_addresses => 'localhost',
                              max_connections => 100,
                              shared_buffers => '24MB',

                              require => Exec['apt-get update'],
}

# psycopg2 needs to be installed in the virtualenv instead.
# include postgresql::python

# create database
postgresql::database { "ls_schedule": owner => "pg_admin", }

############################################################
# https://github.com/puppetmodules/puppet-module-python
############################################################

# create user and group
group { "www-mgr":
  ensure => present,
  gid => 500,
}
user { "www-mgr":
  ensure => present,
  uid => 500,
  gid => 500,
}

class { "python::dev": 
  version => "2.7",
  require => Exec['apt-get update'],
}

class { "python::venv": 
  owner => "www-mgr", 
  group => "www-mgr",
}

python::venv::isolate { "/usr/local/venv/ls_schedule":
  version      => "2.7",
  requirements => "/usr/local/src/ls_schedule/requirements.txt",
  
  require      => Package['libpq-dev']
}

class { "python::gunicorn": 
  owner => "www-mgr", 
  group => "www-mgr" 
}

python::gunicorn::instance { "ls_schedule": 
  venv            => "/usr/local/venv/ls_schedule",
  src             => "/usr/local/src/ls_schedule",
  django          => true,
  django_settings => "ls_schedule/settings.py",
  version         => "18.0",
}

############################################################
# https://github.com/puppetmodules/puppet-module-nginx.git
############################################################

class { nginx: 
  workers => 1 
}

nginx::site { "ls_schedule":
  domain => "ls_schedule.com",
  aliases => ["www.ls_schedule.com"],
  default_vhost => true,
  upstreams => ["unix:/var/run/gunicorn/ls_schedule.sock"],
  
  root => "/usr/local/src/ls_schedule",
  mediaroot => "/var/www/ls_schedule/static",
  mediaprefix => "/static",
}

############################################################
# create the static directory
# Note: The owner and group is set to 'www-data' because 
# the nginx worker processes is owned by 'www-data'.
############################################################

file { ["/var/www", "/var/www/ls_schedule"]:
    ensure => "directory",
    owner  => "www-data",
    group  => "www-data",
    mode   => 750,
    recurse => true,
}
