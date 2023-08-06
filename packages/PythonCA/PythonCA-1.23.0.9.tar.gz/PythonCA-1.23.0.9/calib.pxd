#!cython
#
cdef extern from "stdarg.h":
    pass

cdef extern from "epicsThread.h":
    struct epicsThreadOSD:
        pass
    ctypedef  epicsThreadOSD *epicsThreadId 

cdef extern from "cadef.h":
    struct oldChannelNotify:
       pass
    struct oldSubscription:
        pass

    ctypedef oldChannelNotify *chid
    ctypedef chid chanId  #/* for when the structures field name is "chid" */
    ctypedef long chtype 
    ctypedef oldSubscription  *evid 
    ctypedef double ca_real 
    ctypedef unsigned capri  
    struct connection_handler_args:
        pass
    
    ctypedef void caCh (connection_handler_args args) 

    struct access_rights_handler_args:
        pass
    
    ctypedef void caArh (access_rights_handler_args args) 
    
    struct event_handler_args:
        void            *usr   # /* user argument supplied with request */
        chanId          chid   # /* channel id */
        long            type   # /* the type of the item returned */ 
        long            count  # /* the element count of the item returned */
        const void      *dbr   # /* a pointer to the item returned */
        int             status  #/* ECA_XXX status of the requested op from the server */

    ctypedef void caEventCallBackFunc (event_handler_args) 

    struct ca_client_context:
        pass
    
    struct exception_handler_args:
        pass
    
    ctypedef void caExceptionHandler (exception_handler_args)
    ctypedef void CAFDHANDLER (void *parg, int fd, int opened) 
    ctypedef unsigned CA_SYNC_GID 
    ctypedef int caPrintfFunc ()
    
    ca_client_context * ca_current_context () 
    int  ca_attach_context ( ca_client_context * context ) 
    int  ca_client_status ( unsigned level ) 
    int  ca_context_status ( ca_client_context *, unsigned level ) 
    
    int  ca_attach_context ( ca_client_context * context ) 
    int  ca_client_status ( unsigned level ) 
    int  ca_context_status ( ca_client_context *, unsigned level ) 

    int  ca_build_and_connect(char *pChanName,
                              char *chtype, unsigned long chsz, 
                              chid * pChanID, void *, caCh * pFunc,
                              void * pArg ) 

    int  ca_search_and_connect( char *pChanName,
                                chid * pChanID, 
                                caCh *pFunc, void * pArg ) 
    
    int  ca_channel_status (epicsThreadId tid) 
    int  ca_clear_event ( evid eventID ) 
    int  ca_add_masked_array_event( chtype type,
                                    unsigned long count,
                                    chid chanId,
                                    caEventCallBackFunc * pFunc,
                                    void * pArg, ca_real p_delta,
                                    ca_real n_delta, ca_real timeout,
                                    evid * pEventID, long mask ) 

    int  ca_pend_io (ca_real timeOut) 
    int  ca_pend (ca_real timeout, int early) 

    void  ca_test_event(event_handler_args) 

    short  ca_field_type (chid chan) 
    unsigned long  ca_element_count (chid chan) 
    const char *  ca_name (chid chan) 
    void  ca_set_puser (chid chan, void *puser) 
    void *  ca_puser (chid chan) 
    unsigned  ca_read_access (chid chan) 
    unsigned  ca_write_access (chid chan) 
    enum channel_state:
        pass
    channel_state ca_state (chid chan) 
    
    int  ca_task_initialize () 
    
    enum ca_preemptive_callback_select:
        #ca_disable_preemptive_callback, ca_enable_preemptive_callback 
        pass

    int ca_context_create (ca_preemptive_callback_select select) 
    void  ca_detach_context ()  

    int  ca_create_channel(
        const char     *pChanName, 
        caCh           *pConnStateCallback, 
        void           *pUserPrivate,
        capri          priority,
        chid           *pChanID
    ) 
    int  ca_change_connection_event    (
        chid       chan,
        caCh *     pfunc
    ) 
    int  ca_replace_access_rights_event (
        chid   chan,
        caArh  *pfunc
    ) 

    int  ca_add_exception_event (
        caExceptionHandler *pfunc,
        void               *pArg
    ) 

    int  ca_clear_channel(
        chid   chanId
    ) 
    
    int  ca_array_put(
        chtype         type,   
        unsigned long  count,   
        chid           chanId,
        const void *   pValue
    ) 

    int  ca_array_put_callback(
        chtype                 type,   
        unsigned long          count,   
        chid                   chanId,
        const void *           pValue,
        caEventCallBackFunc *  pFunc,
        void *                 pArg
    ) 

    int  ca_array_get(
        chtype         type,   
        unsigned long  count,   
        chid           chanId,
        void *         pValue
    ) 

    int  ca_clear_subscription(
        evid eventID
    ) 

    chid  ca_evid_to_chid ( evid id ) 

    int  ca_pend_event (ca_real timeOut) 
    int  ca_pend_io (ca_real timeOut) 
    int  ca_pend (ca_real timeout, int early) 
    int  ca_test_io () 
    int  ca_flush_io () 
    void  ca_signal(
        long errorCode,    
        const char *pCtxStr     
    ) 

    void  ca_signal_with_file_and_lineno(
        long errorCode,    
        const char *pCtxStr,    
        const char *pFileStr,   
        int lineNo     
    ) 

    void  ca_signal_formated (long ca_status,
                              const char *pfilenm, 
                              int lineno, const char *pFormat, ...) 

    unsigned  ca_get_host_name ( chid pChan, 
                                 char *pBuf, unsigned bufLength ) 

    int  ca_add_fd_registration    (
        CAFDHANDLER    *pHandler,
        void           *pArg
    ) 


    int  ca_sg_create (CA_SYNC_GID *  pgid) 
    int  ca_sg_delete (const CA_SYNC_GID gid) 
    int  ca_sg_block (const CA_SYNC_GID gid, ca_real timeout) 
    int  ca_sg_test (const CA_SYNC_GID gid) 
    int  ca_sg_reset(const CA_SYNC_GID gid) 
    int  ca_sg_array_get(
        const CA_SYNC_GID gid,
        chtype type, 
        unsigned long count,
        chid chan,
        void *pValue  
    ) 
    int  ca_sg_array_put(
        const CA_SYNC_GID gid,
        chtype type, 
        unsigned long count,
        chid chan,
        const void *pValue  
    ) 

    int  ca_sg_stat (CA_SYNC_GID gid) 
    
    void  ca_dump_dbr (chtype type, unsigned count, const void * pbuffer) 
    int  ca_v42_ok (chid chan) 
    const char *  ca_version () 
    int  ca_replace_printf_handler (
        caPrintfFunc    *ca_printf_func
    ) 
    unsigned  ca_get_ioc_connection_count () 
    int  ca_preemtive_callback_is_enabled () 
    void  ca_self_test () 
    unsigned  ca_beacon_anomaly_count () 
    unsigned  ca_search_attempts (chid chan) 
    double  ca_beacon_period (chid chan) 
    double  ca_receive_watchdog_delay (chid chan) 
    
