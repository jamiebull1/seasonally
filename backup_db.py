"""Simple backup script to take a snapshot of the live database, save it locally, and mirror it to the local DB.
"""
import os
import subprocess

import arrow


TIMEOUT = 30
LOCAL_DB = 'seasonally'
TMP_FILE = 'latest.dump'


def call(cmd, ignore_warning=False):
    print('$ {}'.format(' '.join(cmd)))
    try:
        subprocess.check_call(cmd, timeout=TIMEOUT)
    except subprocess.CalledProcessError as e:
        if not ignore_warning:
            print(e)
            raise

def main():
    assert TMP_FILE not in os.listdir('.')
    call(['heroku', 'pg:backups:capture'])
    call(['heroku', 'pg:backups:download'])
    call(['pg_restore', '--verbose', '--clean', '--no-acl', '--no-owner',
            '-h', 'localhost',
            '-U', 'postgres',
            '-d', LOCAL_DB,
            TMP_FILE,
        ], ignore_warning=True)
    call(['mv', TMP_FILE, 'db_backups/{date}.{db}.bk'.format(date=arrow.utcnow(), db=LOCAL_DB)])


if __name__ == '__main__':
    main()
