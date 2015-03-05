# -*- coding: utf-8 -*-

from fabric.api import abort
from fabric.api import env
from fabric.api import prompt
from fabric.api import run
from fabric.api import settings
from fabric.api import sudo
from fabric.colors import blue, green, magenta, yellow, red
from fabric.context_managers import hide
from fabric.contrib.console import confirm

import config


__all__ = ['test_sudo', 'add_user', 'add_sudo']


def initialize():
    env.use_ssh_config = True
    env.root_password = None
    if config.SSH_PORT != 22:
        env.port = config.SSH_PORT


def test_sudo():
    """ sudoコマンドのテスト用
    """
    initialize()
    for host in config.HOSTS:
        env.host_string = config.ROOT_USER + '@' + host

        with settings(
                hide('warnings', 'running', 'stdout', 'stderr'),
                warn_only=True
                ):
            already_user = sudo('grep nabetama /etc/passwd')
        if already_user:
            print green('nabetama は既に作成済みなので作りませんでした')
            continue


def is_debian():
    with settings(
            hide('warnings', 'running', 'stdout', 'stderr'),
            warn_only=True
            ):
        isdebian = sudo('uname -a | grep debian')
    if isdebian:
        print blue("OS is debian")
        return True
    print green("OS is not debian")
    return False


def formatting(commands, user):
    return [
            command.format(pub_key=user['pub_key'], user=user['name'])
            for command
            in commands
            ]


def exec_commands(commands):
    map(sudo, commands)


def add_user():
    """ config.HOSTSへuserを追加する
    """
    initialize()
    for host in config.HOSTS:
        env.host_string = config.ROOT_USER + '@' + host
        for user in config.ADD_USERS:
            with settings(
                    hide('warnings', 'running', 'stdout', 'stderr'),
                    warn_only=True
                    ):
                already_user = sudo('grep {user} /etc/passwd'.format(user=user['name']))
            if user['name'] in already_user:
                print magenta(already_user)
                print green('[{host:<15}] {user} は既に作成済みなので作りませんでした'.format(
                    host=host,
                    user=user['name']))
                continue
            create_user = 'adduser {user}'

            if is_debian():
                create_user = 'adduser --disabled-password {user}'
            commands = [
                create_user,
                'mkdir /home/{user}/.ssh',
                'touch /home/{user}/.ssh/authorized_keys',
                'chown -R {user}:{user} /home/{user}/.ssh',
                'chmod -R 700 /home/{user}/.ssh',
                'chmod 600 /home/{user}/.ssh/authorized_keys',
                'echo "{pub_key}" >> /home/{user}/.ssh/authorized_keys',
                ]
            # Format strings of commands.
            commands = formatting(commands, user)
            # Execute!
            exec_commands(commands)


def add_sudo():
    """ config.HOSTSに存在するuserに対してNOPASSWD sudoつける
    """
    initialize()
    for host in config.HOSTS:
        env.host_string = config.ROOT_USER + '@' + host
        for user in config.ADD_USERS:
            if not user['sudo']:
                print green('{user} はsudo対象じゃありません'.format(user=user['name']))
                continue
            with settings(
                    hide('warnings', 'running', 'stdout', 'stderr'),
                    warn_only=True
                    ):
                already_user = sudo(
                    'grep {user} /etc/sudoers'.format(user=user['name'])
                )
            if user['name'] in already_user:
                print magenta(already_user)
                print green('[{host:<15}] {user} は既にsudo済みなので作りませんでした'.format(
                    host=host,
                    user=user['name'])
                    )
                continue
            commands = [
                'usermod -G adm {user}',
                'echo "{pub_key}" >> /root/.ssh/authorized_keys',
                'echo "{user} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers',
                ]
            # Format strings of commands.
            commands = formatting(commands, user)
            # Execute!
            exec_commands(commands)
