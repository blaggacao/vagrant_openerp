#//usr/bin/env python

from fabric.api import *
from fabtools.vagrant import vagrant
from fabtools import deb
from fabtools import require

SOURCES_LIST_CONTENT = '''
deb mirror://mirrors.ubuntu.com/mirrors.txt precise main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt precise-updates main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt precise-backports main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt precise-security main restricted universe multiverse
'''


@task
def openerp():
    '''This task's goal is to install OpenERP 7 on a freshly installed Ubuntu
    12.04 Precise Pangolin machine. It installs PostgreSQL and sets up a base.
    Then, it installs OpenERP package from the editor.'''

    ## Because all vagrant users does not live in the USA
    require.file(
        '/etc/apt/sources.list',
        contents=SOURCES_LIST_CONTENT,
        use_sudo=True
    )

    ## Add OpenERP's editor debian packages repository
    require.deb.source(
        'openerp',
        'http://nightly.openerp.com/7.0/nightly/deb/',
        './'
    )

    ## Installs and configure our PostgreSQL server
    require.postgres.server()
    require.postgres.user(
        'openerp',
        password='0p3n3rp',
        createdb=True,
        createrole=True,
        login=True,
        connection_limit=20
    )
    require.postgres.database('openerp', 'openerp')

    ## OpenERP repository provides not signed packages, we can't use
    ## require.deb.package as it does not permit to force the installation
    ## of unsigned packages
    #require.deb.package('cpenerp')
    if not deb.is_installed('openerp'):
        deb.install('openerp', options=['--force-yes'])