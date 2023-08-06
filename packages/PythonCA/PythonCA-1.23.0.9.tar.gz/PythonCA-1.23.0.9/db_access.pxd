#! cython

cdef extern from "epicsTypes.h":
    int EPICS_MAX_STRING_SIZE=40
    ctypedef char            epicsOldString[40]  
    ctypedef char            epicsInt8 
    ctypedef unsigned char   epicsUInt8 
    ctypedef short           epicsInt16 
    ctypedef unsigned short  epicsUInt16 
    ctypedef epicsUInt16     epicsEnum16 
    ctypedef int             epicsInt32 
    ctypedef unsigned int    epicsUInt32 
    ctypedef long long            epicsInt64 
    #ctypedef unsinged epicsInt64  epicsUInt64 
    
    ctypedef float           epicsFloat32 
    ctypedef double          epicsFloat64 
    ctypedef epicsInt32      epicsStatus 

    ctypedef struct epicsString:
        unsigned    length 
        char        *pString 

    union epicsAny:
        epicsInt8       int8 
        epicsUInt8      uInt8 
        epicsInt16      int16 
        epicsUInt16     uInt16 
        epicsEnum16     enum16 
        epicsInt32      int32 
        epicsUInt32     uInt32 
        epicsFloat32    float32 
        epicsFloat64    float64 
        epicsString     string 

    enum epicsType:
        epicsInt8T
        epicsUInt8T
        epicsInt16T
        epicsUInt16T
        epicsEnum16T
        epicsInt32T
        epicsUInt32T
        epicsFloat32T
        epicsFloat64T
        epicsStringT
        epicsOldStringT

cdef extern from "db_access.h":
    int EPICS_MAX_UNITS_SIZE		=8	
    int EPICS_MAX_ENUM_STRING_SIZE	=26
    int EPICS_MAX_ENUM_STATES		=16	

    ctypedef epicsOldString dbr_string_t 
    ctypedef epicsUInt8 dbr_char_t 
    ctypedef epicsInt16 dbr_short_t 
    ctypedef epicsUInt16	dbr_ushort_t 
    ctypedef epicsInt16 dbr_int_t 
    ctypedef epicsUInt16 dbr_enum_t 
    ctypedef epicsInt32 dbr_long_t 
    ctypedef epicsUInt32 dbr_ulong_t 
    ctypedef epicsFloat32 dbr_float_t 
    ctypedef epicsFloat64 dbr_double_t 
    ctypedef epicsUInt16	dbr_put_ackt_t 
    ctypedef epicsUInt16	dbr_put_acks_t 
    ctypedef epicsOldString dbr_stsack_string_t 
    ctypedef epicsOldString dbr_class_name_t 
