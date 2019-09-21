# SmartyDoc

A workflow for report generation based on Jupyter-Notebook and Weasyprint.

Python-based SVG editor
=======================

There is an utility inclued in the repo that helps to edit and concatenate SVG
files. It is especially directed at scientists preparing final figures
for submission to journal. So far it supports arbitrary placement and
scaling of svg figures and adding markers, such as labels.

See the `blog post <http://neuroscience.telenczuk.pl/?p=331>`_  for a short tutorial.

The full documentation is available 
`here <https://svgutils.readthedocs.io/en/latest/index.html>`_.

Note that the `lxml` library is required.
For the installation to be sucessful, you need development libraries of `libxml2` and `libxslt1`.
On Ubuntu and other Debian-derived Linux distributions you can install them via::

   sudo apt-get install libxml2-dev libxslt-dev

