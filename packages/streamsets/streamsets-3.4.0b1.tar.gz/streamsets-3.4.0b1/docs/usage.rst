.. module:: streamsets

Usage instructions
==================

The examples below assume you've installed the ``streamsets`` library,
:ref:`activated the library <activation>`, and are inside a Python 3.4+ interpreter.


Use of the SDK begins by importing the library. For convenience,
we tend to directly import the classes we need:

.. code-block:: python

    >>> from streamsets.sdk import DataCollector

Next, create an instance of :py:class:`streamsets.sdk.DataCollector`, passing in
the URL of your StreamSets Data Collector instance:

.. code-block:: python

    >>> data_collector = DataCollector('http://localhost:18630')

Credentials
-----------

If no user credentials are passed to :py:class:`streamsets.sdk.DataCollector` when it's being instantiated,
:py:attr:`streamsets.sdk.sdc.DEFAULT_SDC_USERNAME` and :py:attr:`streamsets.sdk.sdc.DEFAULT_SDC_PASSWORD` will be
used for the ``username`` and ``password`` arguments, respectively. If your Data Collector instance is
registered with StreamSets Control Hub, your Control Hub credentials need to be used to instantiate an instance
of :py:class:`streamsets.sdk.ControlHub` before it's passed as an argument to :py:class:`streamsets.sdk.DataCollector`
instead:

.. code-block:: python

    >>> from streamsets.sdk import ControlHub
    >>> control_hub = ControlHub('https://cloud.streamsets.com',
                                 username=<your username>,
                                 password=<your password>)
    >>> data_collector = DataCollector('http://localhost:18630', control_hub=control_hub)

Creating a pipeline
-------------------

Next, you can now get an instance of :py:class:`streamsets.sdk.sdc_models.PipelineBuilder`:

.. code-block:: python

    >>> builder = data_collector.get_pipeline_builder()

We get :py:class:`streamsets.sdk.sdc_models.Stage` instances from this builder by calling
:py:meth:`streamsets.sdk.sdc_models.PipelineBuilder.add_stage`.

See the API reference for this method for details on the arguments it takes.

As shown in the :ref:`first example <first-example>`, the simplest type of pipeline
directs one origin into one destination. For this example, we do this with ``Dev Raw Data Source``
origin and ``Trash`` destination, respectively:

.. code-block:: python

    >>> dev_raw_data_source = builder.add_stage('Dev Raw Data Source')
    >>> trash = builder.add_stage('Trash')

With :py:class:`streamsets.sdk.sdc_models.Stage` instances in hand, we can connect them by using the ``>>`` operator,
and then building a :py:class:`streamsets.sdk.sdc_models.Pipeline` instance with the
:py:meth:`streamsets.sdk.sdc_models.PipelineBuilder.build` method:

.. code-block:: python

    >>> dev_raw_data_source >> trash
    >>> pipeline = builder.build('My first pipeline')

Finally, to add this pipeline to your Data Collector instance, pass it to the
:py:meth:`streamsets.sdk.DataCollector.add_pipeline` method:

.. code-block:: python

    >>> data_collector.add_pipeline(pipeline)


Configuring stages
------------------

In practice, it's rare to have stages in your pipeline that haven't had some configurations
changed from their default values. When using the SDK, the names to use when referring
to these configuration properties can generally be inferred from the StreamSets Data Collector UI (e.g.
``Data Format`` becomes ``data_format``), but they can also be directly inspected in a Python
interpreter using the :py:func:`dir` built-in function on an instance of the
:py:class:`streamsets.sdk.sdc_models.Stage` class:

.. code-block:: python

    >>> dir(dev_raw_data_source)

or by using Python's built-in :py:func:`help` function:

.. code-block:: python

    >>> help(dev_raw_data_source)

.. image:: _static/dev_raw_data_source_help.png

With the attribute name in hand, you can read the value of the configuration:

.. code-block:: python

    >>> dev_raw_data_source.max_line_length
    1024

As for setting the value of the configuration, this can be done in one of two ways
depending on your use case:


Single configurations
~~~~~~~~~~~~~~~~~~~~~

If you only have one or two configurations to update, you can set them using attributes of the
:py:class:`streamsets.sdk.sdc_models.Stage` instance. Continuing in the vein of our example:

.. code-block:: python

    >>> dev_raw_data_source.data_format = 'TEXT'
    >>> dev_raw_data_source.raw_data = 'hi\nhello\nhow are you?'

Multiple configurations
~~~~~~~~~~~~~~~~~~~~~~~

For readability, it's sometimes better to set all attributes simultaneously with
one call to the :py:meth:`streamsets.sdk.sdc_models.Stage.set_attributes` method:

.. code-block:: python

    >>> dev_raw_data_source.set_attributes(data_format='TEXT',
                                           raw_data='hi\nhello\nhow are you?')

Connecting stages
-----------------

As described above, to connect the output of one stage to the input of
another, simply use the ``>>`` operator between two :py:class:`streamsets.sdk.sdc_models.Stage` instances:

.. code-block:: python

    >>> dev_raw_data_source >> trash

For stages with multiple outputs, simply use ``>>`` multiple times:

.. code-block:: python

    >>> file_tail = builder.add_stage('File Tail')
    >>> file_tail >> trash_1
    >>> file_tail >> trash_2

.. image:: _static/file_tail_to_two_trashes.png

It is also possible to connect the output of one stage to the inputs of multiple
stages, as in the image below:

.. image:: _static/dev_data_generator_to_two_trashes.png

To do this, put the :py:class:`streamsets.sdk.sdc_models.Stage` instances to which you'll be
connecting the same output into a list before using the ``>>`` operator:

.. code-block:: python

    >>> trash_1 = builder.add_stage('Trash')
    >>> trash_2 = builder.add_stage('Trash')
    >>> dev_raw_data_source >> [trash_1, trash_2]


Events
------

To connect the event lane of one stage to another, use the ``>=`` operator:

.. code-block:: python

    >>> dev_data_generator >> trash_1
    >>> dev_data_generator >= trash_2

.. image:: _static/dev_data_generator_with_events.png


Error stages
------------

To add an error stage, use :py:meth:`streamsets.sdk.sdc_models.PipelineBuilder.add_error_stage`:

.. code-block:: python

    >>> discard = builder.add_error_stage('Discard')


Importing and Exporting Pipelines
---------------------------------

Simple Data Collector to Data Collector Import-Export Operation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To export a Data Collector pipeline to use in the same or a different Data Collector:

.. code-block:: python

    >>> pipeline_json = sdc.export_pipeline(pipeline=sdc.pipelines.get(title='pipeline name'),
                                            include_plain_text_credentials=True)
    >>> with open('./from_sdc_for_sdc.json') as f:
    >>>     json.dump(pipeline_json, f)

You can import a pipeline from a JSON file into Data Collector in two ways:

1. Import the JSON file into :py:class:`streamsets.sdk.sdc_models.PipelineBuilder` and add the pipeline:

.. code-block:: python

    >>> with open('./from_sdc_for_sdc.json', 'r') as input_file:
    >>>     pipeline_json = json.load(input_file)
    >>>
    >>> sdc_pipeline_builder = sdc.get_pipeline_builder()
    >>> sdc_pipeline_builder.import_pipeline(pipeline=pipeline_json)
    >>> pipeline = sdc_pipeline_builder.build(title='built from imported json file from sdc')
    >>> sdc.add_pipeline(pipeline)

2. Directly import the pipeline:

.. code-block:: python

    >>> pipeline = sdc.import_pipeline(pipeline=pipeline_json)

Exporting pipelines from Data Collector for Control Hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To export a Data Collector pipeline to use in Control Hub, specify the optional argument
``include_library_definitions``.

.. code-block:: python

    >>> pipeline_json = sdc.export_pipeline(pipeline=sdc.pipelines.get(title='pipeline name'),
                                            include_library_definitions=True,
                                            include_plain_text_credentials=True)

Similarly, you can export pipelines from Control Hub using :py:meth:`streamsets.sdk.ControlHub.export_pipelines`.

Importing a pipeline into Control Hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can import a pipeline from a JSON file into Control Hub in two ways:

1. Import the JSON file into :py:class:`streamsets.sdk.sch_models.PipelineBuilder` and publish the pipeline:

.. code-block::  python

    >>> with open('./exported_from_sdc.json', 'r') as input_file:
    >>>     pipeline_json = json.load(input_file)
    >>>
    >>> sch_pipeline_builder = sch.get_pipeline_builder()
    >>> sch_pipeline_builder.import_pipeline(pipeline=pipeline_json)
    >>> pipeline = sch_pipeline_builder.build(title='Modified using Pipeline Builder')
    >>> sch.publish_pipeline(pipeline)

2. Directly import the pipeline:

.. code-block:: python

    >>> pipeline = sch.import_pipeline(pipeline=pipeline_json,
                                       name='Exported from sdc')

Exporting and Importing multiple Pipelines at once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To export multiple pipelines from a Data Collector into a zip archive:

.. code-block:: python

    >>> pipelines_zip_data = sdc.export_pipelines(sdc.pipelines, include_library_definitions=True)
    >>> with open('./sdc_exports_for_sch.zip', 'wb') as output_file:
    >>>     output_file.write(pipelines_zip_data)

To import multiple pipelines into ControlHub from a zip archive:

.. code-block:: python

    >>> with open('./sdc_exports_for_sch.zip', 'rb') as input_file:
    >>>     pipelines_zip_data = input_file.read()
    >>> pipelines = sch.import_pipelines_from_archive(pipelines_file=pipelines_zip_data,
                                                      commit_message='Exported as zip from sdc')

Similarly, you could import multiple pipelines into Data Collector by using
:py:meth:`streamsets.sdk.DataCollector.import_pipelines_from_archive`.
