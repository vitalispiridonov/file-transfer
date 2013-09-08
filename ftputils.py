import ftplib

import os

def mdtree(session, dir):
    if not dir_exists(session, dir):
        try:
            session.mkd(dir)
        except:
            mdtree(session, os.path.dirname(dir))
            session.mkd(dir)


def dir_exists(session, dir):
    try:
        session.cwd(os.path.dirname(dir))
        os.path.basename(dir)

        for f in session.nlst():
            if os.path.basename(dir) == f:
                return True
        return False
    except:
        return False


def dftree(session, dir):
    session.cwd(dir)
    for ftpfile in session.nlst():
        ftpfullfile = "{0}/{1}".format(dir, ftpfile)
        try: 
            session.delete(ftpfullfile)
        except:
            if ftpfile != "." and ftpfile != "..":
                try:
                    session.rmd(ftpfullfile)
                except:
                    dftree(session, ftpfullfile)
                    session.cwd(ftpfullfile)
                    session.rmd(ftpfullfile)