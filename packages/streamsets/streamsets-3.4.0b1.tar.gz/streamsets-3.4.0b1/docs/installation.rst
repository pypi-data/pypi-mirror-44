Installation
============

Using pip
---------

To install the most recent stable release of the library, use your Python 3 installation's instance of `pip`_:

.. code-block:: console

    $ pip3 install streamsets

.. _pip: https://pip.pypa.io


.. _activation:

Activation
----------

After installing for the first time, the library requires
an activation key to be used. This key should be placed in the user configuration
directory under ``~/.streamsets`` in a folder called
``activation``. If not present the first time the library is imported, this
directory will be created for you automatically. If this key is not in place, a
:py:exc:`streamsets.sdk.exceptions.ActivationError`
will be raised whenever you attempt to create an instance of
:py:class:`streamsets.sdk.DataCollector`:

.. code-block:: python

    >>> from streamsets.sdk import DataCollector
    >>> data_collector = DataCollector('http://localhost:18630')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/local/lib/python3.6/site-packages/streamsets/sdk/sdc.py", line 59, in __init__
        **kwargs)
      File "streamsets/sdk/sdc_api.pyx", line 79, in sdk.sdc_api.ApiClient.__init__
      File "streamsets/sdk/sdc_api.pyx", line 85, in sdk.sdc_api.ApiClient._verify_activation
    streamsets.sdk.exceptions.ActivationError: Failed to activate Python SDK for StreamSets (reason: Could not find activation file at /Users/dima/.streamsets/activation/rsa-signed-activation-info.properties or /usr/local/lib/python3.6/site-packages/streamsets/sdk/activation/rsa-signed-activation-info.properties).

If you have an ``rsa-signed-activation-info.properties`` file, simply place it into the directory
referenced above and retry your command. If you don't yet have this file, contact StreamSets Support with
a request for access to the SDK for Python.

Versioning
----------

In general, the major and minor release version of the StreamSets SDK for Python should be greater
than or equal to that of the StreamSets Data Collector and/or StreamSets Control Hub instance that
you'd like to interact with. That is, version ``3.2.0`` of the StreamSets SDK for Python
has been tested against StreamSets Data Collector 3.2.0.0 and StreamSets Control Hub 3.2.0.
Compatibility of the StreamSets SDK for Python against earlier versions of StreamSets
Data Collector and StreamSets Control Hub is provided on a best effort basis.
