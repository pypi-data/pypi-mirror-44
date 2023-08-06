#!cython
import cython
from cadefs import *
from caError import *

cimport db_access
cimport calib

def alarmSeverityString(sevr):
    try:
        return AlarmSeverity.Strings[sevr]
    except:
        return "Unkown Severity"

def alarmStatusString(status):
    try:
        return AlarmStatus.Strings[status]
    except:
        return "Unknown Alarm"

def message(status):
    try:
        return caError._caErrorMsg[caError.CA_EXTRACT_MSG_NO(status)]
    except:
        return str(status)

def dbf_type_is_valid(dbftype):
    return dbftype >= 0 and dbftype <= LAST_TYPE

def dbr_type_is_valid(dbrtype):
    return dbrtype >= 0 and dbrtype <= LAST_BUFFER_TYPE

def dbf_type_to_DBR(dbftype):
    if dbftype>=0 and dbftype <= LAST_TYPE:
        return dbftype
    else:
        return -1

def dbf_type_to_DBR_STS(dbftype):
    if dbftype>=0 and dbftype <= LAST_TYPE:
        return dbftype + LAST_TYPE+1
    else:
        return -1

def dbf_type_to_DBR_TIME(dbftype):
    if dbftype>=0 and dbftype <= LAST_TYPE:
        return dbftype + (LAST_TYPE+1)*2
    else:
        return -1
def dbf_type_to_DBR_GR(dbftype):
    if dbftype>=0 and dbftype <= LAST_TYPE:
        return dbftype + (LAST_TYPE+1)*3
    else:
        return -1
	
def dbf_type_to_DBR_CTRL(dbftype):
    if dbftype>=0 and dbftype <= LAST_TYPE:
        return dbftype + (LAST_TYPE+1)*4
    else:
        return -1

# cdef search_and_connect(    char *pChanName,    chid *pChanID    ):
#     pchid=calib.ca_search_and_connect(name, pChanID, NULL, NULL)
#     return pchid

def search(name, nc, pcallback, args):
    # cdef chid *pchid=NULL;
    # pchid=calib.ca_search_and_connect(name, pchid, None,None)
    # return chid
    raise RuntimeError("not implemeted yet")

def clear(ch_id):
     calib.ca_clear_channel(<calib.chid> ch_id)



