# Setup EPICS installation information
import os,platform,sys

from EPICS_config_common import *

if UNAME == "Darwin":
    from EPICS_config_Darwin import *
    
    # get setting from Environment othewise use default values.
    if EPICSROOT== "":
        #EPICSROOT=os.path.join("/opt/epics/R314")
        #HOSTARCH="darwin-intel"
        EPICSROOT=os.path.join("/opt/epics/R316")
        HOSTARCH="darwin-x86"
    EPICSBASE=os.path.join(EPICSROOT,"base")
    EPICSEXT=os.path.join(EPICSROOT,"extensions")
    WITH_TK=os.environ.get("WITH_TK", True)
    libraries_EPICS=["ca","asHost","Com",]
    if WITH_TK:
        TKINC=os.environ.get("TKINC", 
                             "/System/Library/Frameworks/Tk.framework/Versions/Current/Headers")
        TKLIB=os.environ.get("TKLIB", 
                             "/System/Library/Frameworks/Tk.framework/Versions/Current")
        TCLINC=os.environ.get("TCLINC", 
                              "/System/Library/Frameworks/Tcl.framework/Versions/Current/Headers")
        TCLLIB=os.environ.get("TCLLIB", 
                              "/System/Library/Frameworks/Tcl.framework/Versions/Current")
        if (int(os.uname()[2].split(".")[0]) >= 10):
            libraries_TK=["tkstub8.5","tclstub8.5",]
        else:
            libraries_TK=["tkstub8.4","tclstub8.4",]
elif UNAME == "Linux":
    from EPICS_config_Linux import *
    # get setting from Environment othewise use default values.
    if EPICSROOT== "":
        EPICSROOT=os.path.join("/jk/epics/R314-Current")
        #HOSTARCH="linux-x86_64"
    EPICSBASE=os.path.join(EPICSROOT,"base")
    EPICSEXT=os.path.join(EPICSROOT,"extensions")
    WITH_TK=os.environ.get("WITH_TK", True)

    if WITH_TK:
        TKINC=os.environ.get("TKINC", 
                             "/jk/local/include")
        TKLIB=os.environ.get("TKLIB", 
                             "/jk/local/lib")
        TCLINC=TKINC
        TCLLIB=TKLIB
        libraries_TK=["tk8.5","tcl8.5",]
    else:
        TKINC=""
        TKLIB=""
        TCLINC=""
        TCLLIB=""
        libraries_TK=[]
