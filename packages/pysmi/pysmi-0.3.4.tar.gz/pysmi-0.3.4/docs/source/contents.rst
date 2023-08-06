
SNMP SMI compiler
=================

.. toctree::
   :maxdepth: 2

The PySMI library and tools are designed to parse, verify and transform
`SNMP SMI <https://en.wikipedia.org/wiki/Management_information_base>`_ MIB
modules from their original ASN.1 form into JSON or `pysnmp <http://snmplabs.com/pysnmp/>`_
representation.

Documentation
-------------

.. toctree::
   :maxdepth: 2

   /documentation

Source code & Changelog
-----------------------

Project source code is hosted at `GitHub <https://github.com/etingof/pysmi>`_.
Everyone is welcome to fork and contribute back!

We maintain the detailed :doc:`log of changes </changelog>` to our software.

Download & Install
------------------

.. toctree::
   :maxdepth: 2

   /download

Changes
-------

.. toctree::
   :maxdepth: 1

   /changelog

License
-------

The SNMP SMI library software is distributed under 2-clause BSD License.

.. toctree::
   :maxdepth: 2

   /license

MIB files archive
-----------------

The PySMI project maintains a `collection <http://mibs.snmplabs.com/asn1/>`_
of publicly available ASN.1 MIB files collected on the Internet. You are
welcome to use this MIBs archive however we can't guarantee any degree
of consistency or reliability when it comes to these MIB modules.

The *mibdump.py* tool as well as many other utilities based on PySMI
are programmed to use this MIB repository for automatic download and
dependency resolution.

You can always reconfigure PySMI to use some other remote MIB repository
instead or in addition to this one.

Contact
-------

In case of questions or troubles using SNMP SMI library, please open up an
`issue <https://github.com/etingof/pysmi/issues>`_ at GitHub or ask at
`Stack Overflow <http://stackoverflow.com/questions/tagged/pysmi>`_ .
