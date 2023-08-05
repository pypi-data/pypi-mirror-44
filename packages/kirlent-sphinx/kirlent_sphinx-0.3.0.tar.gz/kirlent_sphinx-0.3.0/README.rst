kirlent_sphinx is a Sphinx extension that is primarily meant to be used with
the `Kırlent`_ educational content management system, although it can be used
as a regular Sphinx extension.

Features
--------

kirlent_sphinx provides the following components:

- An extended ``table`` directive derived from the `Cloud Sphinx Theme`_
  project.

- A ``slide`` directive and corresponding HTML themes using `RevealJS`_
  or `ImpressJS`_.

Getting started
---------------

You can install kirlent_sphinx with pip::

  pip install kirlent_sphinx

To enable it in your project, make the following changes in ``conf.py``:

- Add ``kirlent_sphinx`` to extensions::

    extensions = ["kirlent_sphinx"]

- Set the theme to use revealjs or impressjs using one of the below lines::

    html_theme = "kirlent_revealjs"
    html_theme = "kirlent_impressjs"

- Disable index generation::

    html_use_index = False

Usage
-----

For the extended ``table`` directive, consult the documentation
of the `table_styling`_ extension of the `Cloud Sphinx Theme`_ project.

The ``slide`` directives can support most of the ``data-`` attributes
as described in the documentations of the `RevealJS`_ and `ImpressJS`_
projects.

The themes include `Tailwind`_ utility classes for styling::

  .. slide:: Slide title

     .. container:: columns

        .. container:: column w-1/3 bg-blue-lighter

           - item 1a
           - item 1b

        .. container:: column bg-red-lighter

           - item 2

     .. speaker-notes::

        some extra explanation

License
-------

Copyright (C) 2019 H. Turgut Uyar <uyar@tekir.org>

kirlent_sphinx is released under the BSD license. Read the included
``LICENSE.txt`` file for details.

kirlent_sphinx contains code derived from the `Cloud Sphinx Theme`_ project
which is released under the BSD license. Read the included
``LICENSE_cloud_spheme.txt`` file for details.

kirlent_sphinx contains code derived from the `sphinxjp.themes.revealjs`_
project which is released under the MIT license. Read the included
``LICENSE_sphinxjp.themes.revealjs.txt`` file for details.

kirlent_sphinx contains code from the `RevealJS`_ project which is
released under the MIT license. Read the included ``LICENSE_revealjs.txt``
file for details.

kirlent_sphinx contains code from the `ImpressJS`_ project which is
released under the MIT license. Read the included ``LICENSE_impressjs.txt``
file for details.

kirlent_sphinx contains code from the `Tailwind`_ project which is
released under the MIT license. Read the included ``LICENSE_tailwind.txt``
file for details.

.. _Kırlent: https://gitlab.com/tekir/kirlent/
.. _Cloud Sphinx Theme: https://cloud-sptheme.readthedocs.io/en/latest/
.. _table_styling: https://cloud-sptheme.readthedocs.io/en/latest/lib/cloud_sptheme.ext.table_styling.html
.. _sphinxjp.themes.revealjs: https://github.com/tell-k/sphinxjp.themes.revealjs
.. _RevealJS: https://revealjs.com/
.. _ImpressJS: https://impress.js.org/
.. _Tailwind: https://tailwindcss.com/
