# -*- coding: utf-8 -*-

HOSTS = ['<HOST NAME>',]   # hostname at ~/.ssh/config
ROOT_USER = 'root'
SSH_PORT  = '<SSH PORT>'

ADD_USERS = [
        {
            'name': 'nabetama',
            'pub_key': '<USER SSH PUBLIC KEY>',
            'sudo': True,
        },
    ]
