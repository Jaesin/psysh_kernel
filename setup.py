"""Setup script for psysh_kernel package.
"""
from setuptools import setup

version = '0.1.2'

DISTNAME = 'psysh_kernel'

setup(
  name=DISTNAME,
  version=version,
  description='A PHP kernel for Jupyter/IPython, based on MetaKernel',
  long_description=open('README.md', 'rb').read().decode('utf-8'),
  url='https://github.com/jaesin/psysh_kernel',
  author='Jaesin Mulenex',
  maintainer='Jaesin Mulenex',
  author_email='Jaesin@users.noreply.github.com',
  license='BSD',
  py_modules=[DISTNAME],
  packages=[DISTNAME],
  requires=["metakernel (>=0.20.11)", "jupyter_client (>=4.3.0)", "ipykernel"],
  install_requires=["metakernel>=0.20.11", "jupyter_client>=4.3.0", "ipykernel"],
  data_files=[('share/jupyter/kernels/octave', [
          '%s/kernel.json' % DISTNAME,
          '%s/../assets/logo-32x32.png' % DISTNAME,
          '%s/../assets/logo-64x64.png' % DISTNAME,
      ])],
  package_data={DISTNAME: ['%s/kernel.json']},
  include_package_data=True,
  classifiers=[
    'Intended Audience :: Developers/Presenters',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development',
    'Topic :: Presentation',
    'Topic :: System :: Shells',
  ]
)
