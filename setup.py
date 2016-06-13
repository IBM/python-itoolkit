# from distutils.core import setup
from setuptools import setup
from distutils.core import Extension

setup(
  name='itoolkit',
  version='1.2',
  description='IBM i toolkit',
  long_description='IBM i toolkit',
  # url='https://github.com/pypa/sampleproject',
  author="Tony 'Ranger' Cairns",
  author_email='adc@us.ibm.com',
  license='BSD',
  zip_safe=False,
  packages=['itoolkit',
            'itoolkit/rest',
            'itoolkit/db2',
            'itoolkit/lib',
            'itoolkit/test',
            'itoolkit/sample',],
  data_files = [ ('itoolkit', ['itoolkit/README']),
                 ('itoolkit', ['itoolkit/LICENSE']), 
                 ('itoolkit/doc', ['itoolkit/doc/README']), 
                 ('itoolkit/test', ['itoolkit/test/README']), 
                 ('itoolkit/sample', ['itoolkit/sample/README']), 
               ],
  ext_modules=[Extension('itoolkit/itoollib', ['itoolkit/lib/itoollib.c'])],
)

