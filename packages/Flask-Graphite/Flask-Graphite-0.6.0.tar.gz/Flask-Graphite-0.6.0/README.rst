.. image:: https://raw.githubusercontent.com/numberly/flask-graphite/master/artwork/flask-graphite.png

|

.. image:: https://img.shields.io/pypi/v/flask-graphite.svg
   :target: https://pypi.python.org/pypi/flask-graphite
.. image:: https://img.shields.io/github/license/numberly/flask-graphite.svg
   :target: https://github.com/numberly/flask-graphite/blob/master/LICENSE
.. image:: https://img.shields.io/travis/numberly/flask-graphite.svg
   :target: https://travis-ci.org/numberly/flask-graphite
.. image:: https://img.shields.io/coveralls/numberly/flask-graphite.svg
   :target: https://coveralls.io/github/numberly/flask-graphite
.. image:: https://readthedocs.org/projects/flask-graphite/badge/?version=latest
   :target: https://flask-graphite.readthedocs.io/en/latest/?badge=latest

|

Flask-Graphite grants you the power to push useful metrics for each request
without effort

Documentation: https://flask-graphite.readthedocs.io.


Features
========

* Send metrics to graphite for each request
* Metric name based on the route of the request
* Average processing time, number of requests, and stats about status code for
  each route


Example
=======

Here is a minimal template to use Flask-Graphite in a project.

.. code-block:: python

    from flask import Flask
    from flask_graphite import FlaskGraphite

    app = Flask(__name__)
    FlaskGraphite(app)

Such a simple snippet, combined with a Grafana dashboard, would give you
something like this:

.. image:: artwork/grafana_dashboard.png
   :alt: An example dashboard powered with Flask-Graphite
