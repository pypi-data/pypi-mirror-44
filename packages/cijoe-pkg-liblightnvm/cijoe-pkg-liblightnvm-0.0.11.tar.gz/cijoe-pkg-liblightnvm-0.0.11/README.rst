cijoe-pkg-liblightnvm: cijoe testcases and testplans for liblightnvm
====================================================================

.. image:: https://img.shields.io/pypi/v/cijoe-pkg-liblightnvm.svg
   :target: https://pypi.org/project/cijoe-pkg-liblightnvm
   :alt: PyPI

.. image:: https://travis-ci.com/refenv/cijoe-pkg-liblightnvm.svg?branch=master
   :target: https://travis-ci.com/refenv/cijoe-pkg-liblightnvm
   :alt: Build Status

Install
=======

The package is distributed via PyPi, run the following to command to install:

Install ``cijoe-pkg-liblightnvm`` system-wide via the pip:

.. code-block:: bash

  sudo pip install cijoe-pkg-liblightnvm

Or install it user-level:

.. code-block:: bash

  pip install --user cijoe-pkg-liblightnvm

.. note::

  When doing user-level install, then include the :code:`pip` binary install
  path in your :code:`PATH` definition. For example
  :code:`PATH="$PATH:$HOME/.local/bin"`

Create environment definition for CIJOE
=======================================

Run CIJOE interactively and define the target environment:

.. code-block:: bash

  # Start cijoe
  cijoe

  # Use refence definitions as a template for defining your environment
  cat $CIJ_ENVS/refenv-u1604.sh > target_env.sh
  tail -n +2 $CIJ_ENVS/refenv-liblightnvm.sh >> target_env.sh

  # Open up your favorite editor and modify accordingly
  vim target_env.sh

Create virtual environment definition for CIJOE
===============================================

Run CIJOE interactively and define the target environment:

.. code-block:: bash

  # Start cijoe
  cijoe

  # Use refence definitions as a template for defining your environment
  cat $CIJ_ENVS/refenv-u1604.sh > target_env.sh

  # The following is the qemu variables to define
  tail -n +2 $CIJ_ENVS/qemu.sh >> target_env.sh

  # Lastly, the variables used by liblightnvm testcases
  tail -n +2 $CIJ_ENVS/refenv-liblightnvm.sh >> target_env.sh

  # Open up your favorite editor and modify accordingly
  vim target_env.sh

Running tests
=============

Start the test-runner and view the report:

.. code-block:: bash

  # Create directory to store results
  RESULTS=$(mktemp -d trun.XXXXXX -p /tmp)

  # Run using the testplan for Open-Channel 2.0 devices
  cij_runner \
      $CIJ_TESTPLANS/OCSSD_S20_IOCTL.plan \
      target_env.sh \
      --output $RESULTS

  # Create test report
  cij_reporter $RESULTS

  # Inspect the test-report
  xdg-open $RESULTS/report.html

If you find bugs or need help then feel free to submit an `Issue`_. If you want
to get involved head over to the `GitHub page`_ to get the source code and
submit a `Pull request`_ with your changes.

.. _Quickstart Guide: https://cijoe-pkg-liblightnvm.readthedocs.io/en/latest/quickstart.html
.. _Installation: https://cijoe-pkg-liblightnvm.readthedocs.io/
.. _Usage: https://cijoe-pkg-liblightnvm.readthedocs.io/
.. _GitHub page: https://github.com/refenv/cijoe-pkg-liblightnvm
.. _Pull request: https://github.com/refenv/cijoe-pkg-liblightnvm/pulls
.. _Issue: https://github.com/refenv/cijoe-pkg-liblightnvm/issues
