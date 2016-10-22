A Jupyter kernel for Psysh <>

This requires `Jupyter Notebook <http://jupyter.readthedocs.org/en/latest/install.html>`_, and Psysh installed.

To install::

    pip install psysh_kernel
    python -m psysh_kernel.install

To use it, run one of:

.. code:: shell

    ipython notebook
    # In the notebook interface, select Psysh from the 'New' menu
    ipython qtconsole --kernel psysh
    ipython console --kernel psysh

This is based on `MetaKernel <http://pypi.python.org/pypi/metakernel>`_,
which means it features a standard set of magics.

A sample notebook is available online_.

You can specify the path to your Psysh executable by creating an `PSYSH_EXECUTABLE` environmental variable.

.. _online: http://nbviewer.ipython.org/github/Jaesin/psysh_kernel/blob/master/psysh_kernel.ipynb
