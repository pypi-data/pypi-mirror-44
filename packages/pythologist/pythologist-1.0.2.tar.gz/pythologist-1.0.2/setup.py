from setuptools import setup, find_packages
from codecs import open
from os import path

this_folder = path.abspath(path.dirname(__file__))
with open(path.join(this_folder,'README.md'),encoding='utf-8') as inf:
  long_description = inf.read()

setup(
  name='pythologist',
  version='1.0.2',
  test_suite='nose2.collector.collector',
  description='inForm PerkinElmer Reader - Python interface to read outputs of the PerkinElmer inForm software',
  long_description=long_description,
  url='https://github.com/jason-weirather/pythologist',
  author='Jason L Weirather',
  author_email='jason.weirather@gmail.com',
  license='Apache License, Version 2.0',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'License :: OSI Approved :: Apache Software License'
  ],
  keywords='bioinformatics',
  packages=['pythologist'],
  install_requires=['pandas>=0.23.0',
                    'numpy',
                    'scipy',
                    'h5py',
                    'imageio',
                    'tables',
                    'pythologist-image-utilities>=1.0.2'],
  extras_require = {
        'test':  ["pythologist-test-images"]
  },
)
