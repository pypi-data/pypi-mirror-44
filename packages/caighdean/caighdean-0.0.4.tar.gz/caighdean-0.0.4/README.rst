python-caighdean
================

Python client for the Caighdean Machine Translation service -
https://github.com/kscanne/caighdean

|build| |coverage|


Install
-------

.. code-block:: console

  $ pip install caighdean


For development install

.. code-block:: console

  $ pip install -e git+git@github.com:translate/python-caighdean#egg=caighdean
  $ pip install caighdean[test]


Run
---

.. code-block:: python

   >>> import caighdean

   >>> source = u'Agus thubhairt e, \n "Iongantach!" an dèidh sin.'

   >>> source
   u'Agus thubhairt e, \n "Iongantach!" an d\xc3\xa8idh sin.'

   >>> caighdean.Translator().translate(source)
   u'Agus d\xfairt s\xe9, \n "Iontach!" ina dhiaidh sin.'

   >>> print(caighdean.Translator().translate(source))
   Agus dúirt sé,
    "Iontach!" ina dhiaidh sin.


.. |build| image:: https://img.shields.io/travis/translate/python-caighdean/master.svg?style=flat-square
        :alt: Build Status
        :target: https://travis-ci.org/translate/python-caighdean/branches


.. |coverage| image:: https://img.shields.io/codecov/c/github/translate/python-caighdean/master.svg?style=flat-square
        :target: https://codecov.io/gh/translate/python-caighdean/branch/master
        :alt: Test Coverage
