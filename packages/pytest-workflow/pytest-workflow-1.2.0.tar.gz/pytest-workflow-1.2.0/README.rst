===============
pytest-workflow
===============

.. Badges have empty alts. So nothing shows up if they do not work.
.. This fixes readthedocs issues with badges.
.. image:: https://img.shields.io/pypi/v/pytest-workflow.svg
  :target: https://pypi.org/project/pytest-workflow/
  :alt:

.. image:: https://img.shields.io/conda/v/bioconda/pytest-workflow.svg
  :target: https://bioconda.github.io/recipes/pytest-workflow/README.html
  :alt:

.. image:: https://img.shields.io/pypi/pyversions/pytest-workflow.svg
  :target: https://pypi.org/project/pytest-workflow/
  :alt:

.. image:: https://img.shields.io/pypi/l/pytest-workflow.svg
  :target: https://github.com/LUMC/pytest-workflow/blob/master/LICENSE
  :alt:

.. image:: https://api.codacy.com/project/badge/Grade/f8bc14b0a507429eac7c06194fafcd59
  :target: https://www.codacy.com/app/LUMC/pytest-workflow?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LUMC/pytest-workflow&amp;utm_campaign=Badge_Grade
  :alt:

.. image:: https://travis-ci.org/LUMC/pytest-workflow.svg?branch=develop
  :target: https://travis-ci.org/LUMC/pytest-workflow
  :alt:

.. image:: https://codecov.io/gh/LUMC/pytest-workflow/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/LUMC/pytest-workflow
  :alt:

pytest-workflow is a pytest plugin that aims to make pipeline/workflow testing easy
by using yaml files for the test configuration.

For our complete documentation checkout our
`readthedocs page <https://pytest-workflow.readthedocs.io/>`_.


Installation
============
Pytest-workflow requires Python 3.5 or higher. It is tested on Python 3.5, 3.6
and 3.7. Python 2 is not supported.

- Make sure your virtual environment is activated.
- Install using pip ``pip install pytest-workflow``
- Create a ``tests`` directory in the root of your repository.
- Create your test yaml files in the ``tests`` directory.

Pytest-workflow is also available as a `conda package on bioconda
<https://bioconda.github.io/recipes/pytest-workflow/README.html>`_. Follow
`these instructions <https://bioconda.github.io/index.html#set-up-channels>`_
to set up channels properly in order to use bioconda. After that ``conda
install pytest-workflow`` can be used to install pytest-workflow.

Quickstart
==========

Run ``pytest`` from an environment with pytest-workflow installed.
Pytest will automatically gather files in the ``tests`` directory starting with
``test`` and ending in ``.yaml`` or ``.yml``.

To check the progress of a workflow while it is running you can use ``tail -f``
on the ``stdout`` or ``stderr`` file of the workflow. The locations of these
files are reported in the log as soon as a workflow is started.

For debugging pipelines using the ``--kwd`` or ``--keep-workflow-wd`` flag  is
recommended. This will keep the workflow directory and logs after the test run
so it is possible to check where the pipeline crashed. The ``-v`` flag can come
in handy as well as it gives a complete overview of succeeded and failed tests.

Below is an example of a YAML file that defines a test:

.. code-block:: yaml

  - name: Touch a file
    command: touch test.file
    files:
      - path: test.file

This will run ``touch test.file`` and check afterwards if a file with path:
``test.file`` is present. It will also check if the ``command`` has exited
with exit code ``0``, which is the only default test that is run. Testing
workflows that exit with another exit code is also possible. Several other
predefined tests as well as custom tests are possible.

Documentation for more advanced use cases can be found on our
`readthedocs page <https://pytest-workflow.readthedocs.io/>`_.
