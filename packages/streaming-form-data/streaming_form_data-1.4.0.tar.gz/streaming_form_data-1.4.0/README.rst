Streaming multipart/form-data parser
====================================

.. image:: https://travis-ci.org/siddhantgoel/streaming-form-data.svg?branch=stable
    :target: https://travis-ci.org/siddhantgoel/streaming-form-data

.. image:: https://badge.fury.io/py/streaming-form-data.svg
    :target: https://pypi.python.org/pypi/streaming-form-data

.. image:: https://readthedocs.org/projects/streaming-form-data/badge/?version=latest
    :target: https://streaming-form-data.readthedocs.io/en/latest/


:code:`streaming_form_data` provides a Python parser for parsing
:code:`multipart/form-data` input chunks (the most commonly used encoding when
submitting data over HTTP through HTML forms).

Installation
------------

.. code-block:: bash

    $ pip install streaming-form-data

In case you prefer cloning the Github repository and installing manually, please
note that :code:`master` is the development branch, so :code:`stable` is what
you should be working with.

Usage
-----

.. code-block:: python

    >>> from streaming_form_data import StreamingFormDataParser
    >>> from streaming_form_data.targets import ValueTarget, FileTarget, NullTarget
    >>>
    >>> headers = {'Content-Type': 'multipart/form-data; boundary=boundary'}
    >>>
    >>> parser = StreamingFormDataParser(headers=headers)
    >>>
    >>> parser.register('name', ValueTarget())
    >>> parser.register('file', FileTarget('/tmp/file.txt'))
    >>> parser.register('discard-me', NullTarget())
    >>>
    >>> parser.data_received(chunk)

Documentation
-------------

Up-to-date documentation is available on `Read the Docs`_.

Development
-----------

Please make sure you have Python 3.4+ installed.

1. Git clone the repository -
   :code:`git clone https://github.com/siddhantgoel/streaming-form-data`

2. Install the packages required for development -
   :code:`make local`

3. That's basically it. You should now be able to run the test suite -
   :code:`py.test`.

Please note that :code:`tests/test_parser_stress.py` stress tests the parser
with large inputs, which can take a while. As an alternative, pass the filename
as an argument to :code:`py.test` to run tests selectively.


.. _pip tools: https://github.com/jazzband/pip-tools
.. _Read the Docs: https://streaming-form-data.readthedocs.io/
