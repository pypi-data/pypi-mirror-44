YouTrack Python 3 Client Library
================================

|build| |pypi| |codacy| |license|

This document describes Python 3 library that wraps YouTrack REST API.

Compatibility

Current implementation of the YouTrack Python 3 Client Library and
scripts is compatible with YouTrack 3.x and higher REST API and Python
3.

Installation
------------

To install YouTrack Python 3 Client Library:

.. code:: python

      pip install dohq-youtrack

Authenticating
--------------

.. code:: python

      from youtrack.connection import Connection
      connection = Connection('http://teamsys.intellij.net', 'xxx', 'xxx')

Get Issues
----------

.. code:: python

      # get one issue
      connection.get_issue('SB-1')

.. code:: python

      # get first 10 issues in project JT for query 'for: me #unresolved'
      connection.get_issues('JT', 'for: me #unresolved', 0, 10)

      # get issues from all projects
      connection.get_all_issues('for: me #unresolved', 0, 10)

Create Issue
------------

.. code:: python

      connection.create_issue('SB', 'resttest', 'Test issue', 'Test description', '2', 'Bug', 'First', 'Open', '', '', '')

Other Methods
-------------

See method of class Connection in
`youtrack/connection.py <https://github.com/devopshq/youtrack/blob/master/youtrack/connection.py>`__


.. |build| image:: https://travis-ci.org/devopshq/youtrack.svg?branch=master   :target: https://travis-ci.org/devopshq/youtrack
.. |pypi| image:: https://img.shields.io/pypi/v/dohq-youtrack.svg   :target: https://pypi.python.org/pypi/dohq-youtrack
.. |codacy| image:: https://api.codacy.com/project/badge/Grade/9f6d2c74eb1a4d798b87bd05bed6ee21   :target: https://www.codacy.com/app/devopshq/youtrack
.. |license| image:: https://img.shields.io/pypi/l/dohq-youtrack.svg   :target: https://github.com/devopshq/youtrack/blob/master/LICENSE