#!/usr/bin/env python
"""
Setup file for Ca-Python using distutils package.
Python2.4 or later should be used.

Version Info: (before 1.22)
  $HGTagShort: 1.23.0.9 $
  $lastlog: compatiblity with both EPICS R3.1.4 and R3.1.6 $

  Revision 1.22  2010/08/18 06:46:32  noboru
  support python3

  Revision 1.6  2007/03/20 11:48:56  noboru
  Add RCS keywords to setup.py
"""
## start normal setup.
#from distutils.core import setup,Extension
from distutils.core import setup
# for cython
from Cython.Distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize


import os,platform,sys
try:
    UNAME=platform.system()
except:
    UNAME="Unknowon"

# macros managedd by mercurial keyword extension
CVSAuthor="$Author: noboru $"
CVSDate="$Date: 2019/04/12 02:48:25 $"
CVSRev="$Revision: 4345510ff0bf $"
CVSSource="$Header: /Users/noboru/src/python/VXI11/PyVXI11-Current/cVXI11_revision.py,v 4345510ff0bf 2019/04/12 02:48:25 noboru $"
CVSFile="$Source: /Users/noboru/src/python/VXI11/PyVXI11-Current/cVXI11_revision.py,v $"
CVSId="$Id: cVXI11_revision.py,v 4345510ff0bf 2019/04/12 02:48:25 noboru $"
#
HGTag="$HGTag: 1.23.0.9-05c09e6a914c $"
HGdate="$HGdate: Sat, 13 Apr 2019 16:38:04 +0900 $"
HGTagShort="$HGTagShort: 1.23.0.9 $"
HGlastlog="$lastlog: compatiblity with both EPICS R3.1.4 and R3.1.6 $"
#
rev=HGTag[HGTag.index(":")+1:HGTag.index("-")].strip()

release = os.popen("hg log -r tip --template '{latesttag}.{latesttagdistance}-{node|short}'").read()

try:
    from EPICS_config_local import *
except ImportError:
    try:
        if (UNAME == "Darwin"):
            from EPICS_config_Darwin import *
        elif(UNAME =="Linux"):
            from EPICS_config_Linux import *
        elif(UNAME =="Windows"):
            from EPICS_config_Win32 import *
        else:
            sys.stderr.write("No config file. Retain Environment variable setting.")
            sys.exit()
    except ImportError:
        sys.stderr.write("No config file. Retain Environment variable setting.")
        sys.exit()
        
# check if EPICS envrionment are set properly.
try:
    assert(EPICSROOT)
    assert(EPICSBASE)
    assert(EPICSEXT)
except AssertionError:
    sys.stderr.write("Please setup EPICS environment(EPICSROOT)\n")
    sys.exit()
                     
if (HOSTARCH==None):
    HOSTARCH=os.popen(os.path.join(EPICSBASE,"startup/EpicsHostArch.pl")).read()
else:
    sys.stderr.write("HOSTARCH:{}\n".format(HOSTARCH))
    sys.stderr.write("TKINC:{}\n".format(TKINC))
    
assert(HOSTARCH)

# create EPICSverion.py
import makeEpicsVersion

makeEpicsVersion.mkEpicsVersion(
    "epicsVersion.py"
    ,os.path.join(EPICSBASE,"include/epicsVersion.h")
    ,"" #opt_version
    , False #opt_q
    , False #opt_V
)

from epicsVersion import EPICS_VERSION_INFO

# choose _ca source
#CA_SOURCE="_ca.c"  # for NON-threaded version
CA_SOURCE="_ca314.cpp" # for threaded version.

extra={}
# if sys.version_info >= (3,):
#     extra['use_2to3'] = True

try:
   from distutils.command.build_py import build_py_2to3 as build_py #for Python3
except ImportError:
   from distutils.command.build_py import build_py     # for Python2


# mercurial keyword. usr 'hg ci' and 'hg kwexpand' to update the following keywords
#
sys.stderr.write("{}\n".format(EPICS_VERSION_INFO))

if EPICS_VERSION_INFO >= (3,16):  # 
    libraries_EPICS=["ca","Com"] 
else:
    libraries_EPICS=["ca","Com"] 
    
libraries=libraries_EPICS+libraries_TK

if (libraries==None):
    if UNAME.lower() == "alpha":#?
        libraries=["ca","As","Com"]
    else:
        WITH_TK=True
        libraries=["ca","asHost","Com","tk","tcl",]

if WITH_TK:
    tk_include_dir=[os.path.join(TKINC, "include") for pth in (TKINC, TCLINC) if pth]
    tk_include_dir += [os.path.join(TKINC,) for pth in (TKINC, TCLINC) if pth]
else:
    tk_include_dir=[]
#
# calib3.pyx is actually hard link to calib.pyx
# 
if sys.version_info < (3,):
    calib_source="calib.pyx"
else:#python3 or later
    calib_source="calib3.pyx"
    if not os.path.exists(calib_source):
        os.link('calib.pyx',calib_source)
    
calib_ext= Extension(
    "calib",[calib_source, ],
    depends=["setup.py","calib.pxd"],
    include_dirs=tk_include_dir+[
        os.path.join(EPICSBASE,"include"),
        os.path.join(EPICSBASE,"include/os",UNAME),
        os.path.join(EPICSBASE,"include/os"),
        os.path.join(EPICSBASE,"include/compiler"),
        os.path.join(EPICSBASE,"include/compiler/{}".format(CMPLR_CLASS)),
        os.path.join("/usr/X11R6","include"),
        os.path.join("/usr/X11/include","include"),
    ],
    define_macros=[("PYCA_VERSION","\"%s\""%rev),
                   ("PYCA_HG_RELEASE","\"%s\""%release),
                   ("WITH_THREAD", None),
                   ("WITH_TK", WITH_TK),
                   ("UNIX", None),
                   (UNAME, None)],
    undef_macros="CFLAGS",
    language="c++",
    libraries=libraries,
    library_dirs=[os.path.join(EPICSBASE,"lib",HOSTARCH),
    ] + [os.path.join(path,"") for path in (TKLIB,TCLLIB) if path],
    extra_compile_args=["-O"], # Can we set it to -O1 ?
    runtime_library_dirs=[os.path.join(EPICSBASE,"lib",HOSTARCH),],
)

setup(name="PythonEPICS-CA",
      version=rev,
      author="Noboru Yamamoto, KEK, JAPAN",
      author_email = "Noboru.YAMAMOTO@kek.jp",
      description="EPICS CA library interface module with Cython",
      long_description="""
      EPICS CA library interface module (KEK, Japan)
      """,
      url="http://www-acc.kek.jp/EPICS_Gr/products.html",
      download_url="http://www-acc.kek.jp/EPICS_Gr/products.html",
      classifiers=['Programming Language :: C++',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.7',
                   'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
                   ],
      py_modules=[],
      ext_modules=cythonize(calib_ext),
)

ca_ext= Extension(
    "_ca", [CA_SOURCE, ],
    depends=["setup.py",],
    include_dirs=tk_include_dir+[
        os.path.join(EPICSBASE,"include"),
        os.path.join(EPICSBASE,"include/os",UNAME),
        os.path.join(EPICSBASE,"include/os"),
        os.path.join(EPICSBASE,"include/compiler"),
        os.path.join(EPICSBASE,"include/compiler/{}".format(CMPLR_CLASS)),
        os.path.join("/usr/X11R6","include"),
        os.path.join("/usr/X11","include"),
    ],
    define_macros=[("PYCA_VERSION","\"%s\""%rev),
                   ("PYCA_HG_RELEASE","\"%s\""%release),
                   ("WITH_THREAD", None),
                   ("WITH_TK", WITH_TK),
                   ("UNIX", None),
                   (UNAME, None)],
    undef_macros="CFLAGS",
    language="c++",
    libraries=libraries,
    library_dirs=[os.path.join(EPICSBASE,"lib",HOSTARCH),
    ] + [os.path.join(path,"") for path in (TKLIB,TCLLIB) if path],
    extra_compile_args=["-O"], # Can we set it to -O1 ?
    runtime_library_dirs=[os.path.join(EPICSBASE,"lib",HOSTARCH),],
)

ext_modules=cythonize([ca_ext,calib_ext])

#
setup(name="PythonCA",
      version=rev,
      author="Noboru Yamamoto, KEK, JAPAN",
      author_email = "Noboru.YAMAMOTO@kek.jp",
      description="EPICS CA library interface module",
      long_description="""
      EPICS CA library interface module (KEK, Japan)
      """,
      url="http://www-acc.kek.jp/EPICS_Gr/products.html",
      download_url="http://www-acc.kek.jp/EPICS_Gr/products.html",
      classifiers=['Programming Language :: C++',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
                   #'Topic :: EPICS CA',
                   #'Topic :: Controls'
                   ],
      py_modules=["ca", "caError", "cadefs","_ca_kek","_ca_fnal","CaChannel","printfn","epicsVersion"],
      ext_modules=ext_modules,
      **extra
)

setup(name="cas",
      version=rev,
      author="Tatsuro Nakamura, KEK, JAPAN",
      author_email = "Tatsuro.nakamura@kek.jp",
      description="EPICS CA library interface module",
      long_description="""
      Simple EPICS CA library interface module (KEK,Japan)
      """,
      url="http://www-acc.kek.jp/EPICS_Gr/products.html",
      download_url="http://www-acc.kek.jp/EPICS_Gr/products.html",
      classifiers=['Programming Language :: Python :: 2.7',
                   'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
                   #'Topic :: EPICS CA',
                   #'Topic :: Controls'
                   ],
      package_dir={"":"cas"},
      py_modules=["cas","xca"],
      **extra
)
