# Setup EPICS installation information
"""
Configuration file for EPICS installation.
"""
import os,platform,sys

try:
    UNAME=platform.uname()[0]
except:
    UNAME="Unknowon"
    
# get setting from Environment othewise use default values.
EPICSROOT=os.environ.get("EPICS_ROOT",
                         os.environ.get("EPICSROOT", 
                                        ""
                         ))
if EPICSROOT =="":
    if os.environ.get('EPICS_BASE',False):
        EPICSROOT=os.path.split(os.environ['EPICS_BASE'].rstrip(os.path.sep))[0]
    elif os.environ.get('EPICSBASE',False):
        EPICSROOT=os.path.split(os.environ['EPICSBASE'].rstrip(os.path.sep))[0]
    else:
        EPICSROOT=""

#
EPICSBASE=os.environ.get("EPICS_BASE",
                         os.environ.get("EPICSBASE",
                                        os.path.join(EPICSROOT,"base")
                         ))
EPICSEXT=os.environ.get("EPICS_EXTENSIONS", 
                        os.environ.get("EPICSEXT", 
                                       os.path.join(EPICSROOT,"extensions")
                        ))
HOSTARCH=os.environ.get("HOSTARCH",
                        "{}-{}".format(platform.system().lower(),
                                       platform.machine().lower()
                        ))
WITH_TK=os.environ.get("WITH_TK",False)

TKINC=os.environ.get("TK_INC", "")
TKLIB=os.environ.get("TK_LIB", "")
TCLINC=TKINC
TCLLIB=TKLIB

