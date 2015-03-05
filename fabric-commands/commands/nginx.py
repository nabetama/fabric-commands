# coding: utf-8
import config
import os
from fabric.api import sudo, roles
from fabric.colors import green, red
from .create_users import initialize 


def yum_install():
    commands = [
        'sudo yum install memcached',
        ]
    map(sudo, commands)


def edit_nginx_setting():
    # TODO: customize
    commands = [
        'ps aux | grep nginx | grep -v ps',
        '/etc/init.d/nginxd restart',
        'ps aux | grep nginxd | grep -v ps',
        ]
    map(sudo, commands)


@roles('nginx')
def install_nginx():
    """ nginx install
    """
    # TODO: host,  roles.
    yum_install()
    edit_nginx_setting()
    return True

