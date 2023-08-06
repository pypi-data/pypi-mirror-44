#!/bin/env python
#-*- coding: utf-8 -*-
# based on makeEPicsVersion.pl
# copyright notice for makeEPicsVersion.pl
#*************************************************************************
# Copyright (c) 2012 UChicago Argonne LLC, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2002 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# EPICS BASE is distributed subject to a Software License Agreement found
# in file LICENSE that is included with this distribution. 
#*************************************************************************
#
#  makeEPicsVersion.py was written by N.Yamamoto@kek.jp (c) 2016.12.12
#
import sys,os,os.path
import argparse
import re

OUTPUT_HELP_VERSION = 1

def main():
    tool = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        description='make EPICS version files for configuration setting'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-q","--quiet",action='store_true',
                        help="Quiet: Only print errors",
    )
    group.add_argument("-V","--Verbose",action='store_true',
                        help="Verbose: print anything",
    )
    parser.add_argument("-o","--output",action='store',default='epicsVersion.py',metavar='<Output File>',
                        help="Output filename [default:epicsVersion.py]",
    )
    parser.add_argument("-v","--version",action='store',metavar='<Version String>',
                        help="Site-specific version string",
    )
    parser.add_argument('config_base_version',default="epicsVersion.h")

    try:
        args = parser.parse_args()
        mkEpicsVersion(args.output, args.config_base_version, args.version,
                       args.quiet, args.Verbose)
    except:
        pass

def mkEpicsVersion(opt_o, infile, opt_version, opt_q, opt_V):

    if opt_o and not opt_q :
        print ("Building {} from {}.".format(opt_o, infile))

    ver=rev=mod=patch=snapshot=commit_date=""
    dct={}
    with open(infile,"r") as f:
        for l in f:
            l=l.strip()
            if re.match("^#/\*",l): continue # skip comment 
            if not re.match("^#define.*",l): continue # skip non define
            m=re.match("^#define\s+([\w]+)\s+(\d+)",l); # defines name and integer
            if m: dct[m.groups()[0].strip()]=int(m.groups()[1]); continue
            m=re.match("^#define\s+([\w]+)\s+([\'\"].*[\'\"])",l); # defines string constats. quote in  is not supported
            if m: dct[m.groups()[0].strip()]=m.groups()[1]; continue
            continue
        
        if opt_version:
            dct["EPICS_SITE_VERSION"]=dct.get("EPICS_SITE_VERSION",'""')+' "{}"'.format(opt_version)

        dct["EPICS_VERSION_INFO"]=(
            dct["EPICS_VERSION"],
            dct["EPICS_REVISION"],
            dct["EPICS_MODIFICATION"],
            dct["EPICS_PATCH_LEVEL"])
        
        if opt_V:
            for e in dct:
                print (e, dct[e],type(dct[e]))
                
        with open(opt_o,'w') as o:
            obase=os.path.extsep.join((os.path.splitext(opt_o)[0],"py"))
            o.write("""#!python
            \n# -*- coding:utf-8 -*-
            \n# EPICS version info from {}
            \n""".format(infile,)
            )
            for e in dct:
                o.write("{} = {}\n".format(e,dct[e]))
            
if __name__ == "__main__":
    main()
    
