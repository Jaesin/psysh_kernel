[![Build Status](https://travis-ci.org/Jaesin/psysh_kernel.svg?branch=master)](https://travis-ci.org/Jaesin/psysh_kernel)

### A Jupyter kernel for PsySH

This requires **Jupyter Notebook** <http://jupyter.readthedocs.org/en/latest/install.html> 
and [PsySH](http://psysh.org/) installed.

To install:

```bash
pip install psysh_kernel
python -m psysh_kernel.install
```

To use it, run one of:

```bash

ipython notebook
# In the notebook interface, select Psysh from the 'New' menu
ipython qtconsole --kernel psysh
ipython console --kernel psysh
```

This is based on MetaKernel <http://pypi.python.org/pypi/metakernel> 
which means it features a standard set of magics.

A sample notebook is available [online](https://github.com/Jaesin/psysh_kernel/blob/master/psysh_kernel.ipynb).

You can specify the path to your Psysh executable by creating an 
`PSYSH_EXECUTABLE` environmental variable.

### Thanks

Thanks to the metakernel project (<https://github.com/Calysto/metakernel>) 
and it's [contributers](https://github.com/Calysto/metakernel/graphs/contributors).
