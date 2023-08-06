from setuptools import setup, find_packages
from codecs import open
from os import path

this_folder = path.abspath(path.dirname(__file__))
with open(path.join(this_folder,'README.md'),encoding='utf-8') as inf:
  long_description = inf.read()

setup(
  name='pythologist-image-utilities',
  version='1.0.2',
  test_suite='nose2.collector.collector',
  description='Functions to assist in working with image files',
  long_description=long_description,
  url='https://github.com/jason-weirather/pythologist-image-utilities',
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
  packages=['pythologist_image_utilities'],
  install_requires=['pandas>=0.23.0',
                    'numpy',
                    'scikit-image',
                    'scipy']
)
