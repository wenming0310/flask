# -*- coding: utf-8 -*-

"""
fabfile.py
~~~~~~~~~~~~~~~~~~~~

在当前文件路径下, 切换到python的虚拟环境, 运行
fab -l   查看命令并执行相应操作即可

"""

from fabric.api import env, task, local

env.roledefs.update({
    'web1': ['root@47.93.62.100'],
    'web2': ['root@39.106.173.210'],
})

env.passwords = {
    'root@47.93.62.100': 'Trl199123',
    'root@39.106.173.210': 'Trl.1991318'
}

_TAR_FILE = 'go-shop.tar.gz'


@task
def build():
    """
    打包项目
    :return:
    """
    includes = ['app', 'instance', '*.*']
    excludes = ['*.log', '*.pyc', '*.pyo', '.gitignore', 'fabfile.py', 'dev.py', 'manage-dev.py']
    local('rm -f dist/%s' % _TAR_FILE)
    cmd = ['tar', '--dereference', '-czvf', 'dist/%s' % _TAR_FILE]
    cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
    cmd.extend(includes)
    local(' '.join(cmd))
