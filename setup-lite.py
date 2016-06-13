# from distutils.core import setup
from setuptools import setup
from distutils.core import Extension

setup(
  name='itoolkit-lite',
  version='1.2',
  description='IBM i toolkit lite',
  long_description='IBM i toolkit lite',
  # url='https://github.com/pypa/sampleproject',
  author="Tony 'Ranger' Cairns",
  author_email='adc@us.ibm.com',
  license='BSD',
  zip_safe=False,
  packages=['itoolkit',
            'itoolkit/rest',
            'itoolkit/db2',],
  data_files = [ ('itoolkit', ['itoolkit/README']),
                 ('itoolkit', ['itoolkit/LICENSE']), 
                 ('itoolkit/doc', ['itoolkit/doc/README']), 
               ],
)

