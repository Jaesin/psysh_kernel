from setuptools import setup

version = '0.1.2'

setup(name='psysh_kernel',
      version=version,
      description='A PHP kernel for Jupyter/IPython, based on MetaKernel',
      long_description=open('README.md', 'rb').read().decode('utf-8'),
      url='https://github.com/jaesin/psysh_kernel',
      author='Jaesin Mulenex',
      maintainer='Jaesin Mulenex',
      author_email='Jaesin@users.noreply.github.com',
      license='BSD',
      py_modules=['psysh_kernel'],
      requires=["metakernel", "jupyter_client", "ipykernel"],
      install_requires=["metakernel>=0.20.11", "jupyter_client>=4.3.0", "ipykernel"],
      packages=['psysh_kernel'],
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
