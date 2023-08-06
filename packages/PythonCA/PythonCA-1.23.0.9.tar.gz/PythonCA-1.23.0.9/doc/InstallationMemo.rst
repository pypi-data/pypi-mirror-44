Python-CA  installation memo
============================

.. container::

   KEK, High Energy Accelerator Research Organization
   Acceleator Lab
   Noboru Yamamoto

| 

#. This program is retistered in PyPI. 
   #. you need to setup EPICSROOT environment varible before install this program
      using pip command. You may need other environment variables, such as WITH_TK, TKINC, TKLIB, HOSTARCH.
   #. You can create create EPICS_config_local.py files to setup these environment. Put this file in 
      somewhere in your PYTHONPATH.
#. You need Python 2.7 or later and EPICS 3.14.7 or later. (It may work
   with older version, but these are oldest versions I have built.) 
#. Get a Python-CA extension module package as `a tarball 
   here <CaPython-1.10.tar.gz>`__\ [updated on 2007/05/03].
#.  Expand this tarball at  your working directory.
#. Open setup.py in your favourite editor and change some parametes,
   such as EPICS architechture and installation path, appropriately.

   ::

      EPICSROOT=os.path.join("your epics root path")

   ::

      EPICSBASE=os.path.join(EPICSROOT,"base")

   ::

      EPICSEXT=os.path.join(EPICSROOT,"extensions")

   ::

      HOSTARCH="your epics host architecture"

#. run the installation script, setup.py/  for build extension moules.

   ::

      python setup.py build

#. if you encounter the compilation errors or any trouble , please send
   a message to  noboru.yamamoto_at_kek.jp.
#. | You need to have write permission of the target directories for
     installation. Run:

   ::

      python setup.py install

#. Test extension module.

.. container::

   start python interpreter.

::

    python

.. container::

   Try to import ca module

::

    import ca

.. container::

   Check access to EPICS DB. (Assuming excas is running.)

::

   ca.Get("fred")

Note to a GUI programmer:
^^^^^^^^^^^^^^^^^^^^^^^^^

| You should not call functions in GUI system(Tkinter or wxPython) in
  the Python-CA callback routines. It will crash your running program
  immediately.
