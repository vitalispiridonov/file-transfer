from fabric.api import *
from ftputils import *

import ftplib
import os.path
import ConfigParser

env.colors = True

def upload():

    conf_file = 'config.default.ini'
    if (os.path.isfile('config.ini')):
        config_file = 'config.ini'

    config = ConfigParser.ConfigParser();
    config.read(config_file);

    section = 'Default'

    ftp_dir = config.get(section, 'ftp.dir')
    ftp_host = config.get(section, 'ftp.host')
    ftp_user = config.get(section, 'ftp.user')
    ftp_pass = config.get(section, 'ftp.pass')
    project_dir = config.get(section, 'project.dir')

    session = ftplib.FTP(ftp_host, ftp_user, ftp_pass)
    dftree(session, ftp_dir)
    local('echo Clear ftp folder')

    for root, dirs, files in os.walk(project_dir): 
        for fname in files:

            full_fname = os.path.join(root, fname)
            ftp_fname = '{0}/{1}'.format(ftp_dir, full_fname.replace(project_dir, ''))

            mdtree(session, os.path.dirname(ftp_fname))

            file = open(full_fname,'rb')
            session.storbinary('STOR {0}'.format(ftp_fname), file)
            file.close()

            local('echo Uploaded {0}'.format(fname))

    session.quit()