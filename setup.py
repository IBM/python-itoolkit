from setuptools import setup, find_packages
from distutils.core import Extension

setup(
  name='itoolkit',
  version='1.5.1',
  description='IBM i toolkit',
  long_description='IBM i toolkit',
  # url='https://github.com/pypa/sampleproject',
  author="Tony 'Ranger' Cairns",
  author_email='adc@us.ibm.com',
  license='BSD',
  zip_safe=False,
  packages=find_packages(),
  data_files = [ ('itoolkit', ['itoolkit/README']),
                 ('itoolkit', ['itoolkit/LICENSE']), 
                 ('itoolkit/doc', ['itoolkit/doc/README']), 
                 ('itoolkit/test', ['itoolkit/test/README']), 
                 ('itoolkit/sample', ['itoolkit/sample/README']), 
               ],
  ext_modules=[Extension('itoolkit/itoollib', ['itoolkit/lib/itoollib.c'])],
)

