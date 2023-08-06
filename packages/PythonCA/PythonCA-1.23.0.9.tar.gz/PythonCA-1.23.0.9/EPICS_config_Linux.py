# Setup EPICS installation information
import os

from EPICS_config_common import *

CMPLR_CLASS='gcc'

if WITH_TK:
    TKINC=os.environ.get("TKINC", "/usr/include")
    TKLIB=os.environ.get("TKLIB", "/usr/lib")
    TCLINC=TKINC
    TCLLIB=TKLIB
    libraries_TK=["tk8.5","tcl8.5",]
else:
    TKINC=""
    TKLIB=""
    TCLINC=""
    TCLLIB=""
    libraries_TK=[]

