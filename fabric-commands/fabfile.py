# -*- coding: utf-8 -*-

from commands.create_users import *
from commands.nginx import install_nginx

from fabric.api import env

env.roledefs['webservers'] = {
        'nginx': {
            'hosts': ['www'],
        }
    }
