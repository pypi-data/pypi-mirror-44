============================
Sphinx Theme for ZEIT ONLINE
============================

Based on the fabulous `Read the Docs`_ theme.

.. _`Read the Docs`: https://github.com/rtfd/sphinx_rtd_theme


Usage
=====

Install the package, e.g. ``pip install sphinx_zon_theme``, and then set
``html_theme = 'sphinx_zon_theme'`` in your Sphinx ``conf.py``.


Features
========

* Automatically uses the ZON logo.
* Adds an "edit this page" link to the sidebar. To customize how this link is
  created, you can set the following::

    html_theme_options = {
        'editme_link': (
            'https://github.com/zeitonline/{project}/edit/master/{page}')
    }

  (This is the default value, it supports two variables, ``project`` is taken
   directly from ``conf.py``, and ``page`` evaluates to
   ``path/to/current/page.suffix``)
* Supports (multi-project) search using `sphinx_elasticsearch`_.
  Configure like this (default values are shown here)::

    html_theme_options = {
        'elasticsearch_host': 'http://docs.zeit.de/elasticsearch',
        'elasticsearch_index': 'docs',
        # For creating links to search result items
        'public_url_root': 'http://docs.zeit.de/'
    }

  To disable and use the built-in Sphinx search, set ``elasticsearch_host`` to None.
* Adds a "like" button (iframe) at the bottom of each page. To disable, set ``like_iframe_src`` to None.

.. _`sphinx_elasticsearch`: https://pypi.org/project/sphinx_elasticsearch
