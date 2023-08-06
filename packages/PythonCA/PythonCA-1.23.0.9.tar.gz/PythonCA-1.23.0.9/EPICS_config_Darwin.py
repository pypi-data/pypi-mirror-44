# Setup EPICS installation information
import os,platform,sys
# import pkgconfig

# if os.system('which pkg-config') <> 0:
#     os.environ["PATH"]+=":/usr/local/bin"

# assert(os.system('which pkg-config')==0)

from EPICS_config_common import *

WITH_TK=True

if WITH_TK:
    TKINC=locals().get("TKINC", 
                         "/System/Library/Frameworks/Tk.framework/Versions/Current/Headers")
    TKLIB=locals().get("TKLIB", 
                         "/System/Library/Frameworks/Tk.framework/Versions/Current")
    TCLINC=locals().get("TCLINC", 
                              "/System/Library/Frameworks/Tcl.framework/Versions/Current/Headers")
    TCLLIB=locals().get("TCLLIB", 
                          "/System/Library/Frameworks/Tcl.framework/Versions/Current")
    libraries_TK=["tkstub8.5","tclstub8.5",]
else:
    TKINC=""
    TKLIB=""
    TCLINC=""
    TCLLIB=""
    libraries_TK=[]
    
CMPLR_CLASS = "clang"
