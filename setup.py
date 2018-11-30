from setuptools import setup, find_packages
from distutils.core import Extension

setup(
    name='itoolkit',
    version='1.5.1',
    description='IBM i XMLSERVICE toolkit for Python',
    long_description='IBM i XMLSERVICE toolkit for Python',
    url='https://bitbucket.org/litmis/python-itoolkit',
    author="IBM",
    license='MIT',
    zip_safe=False,
    packages=find_packages(),
    data_files = [
        ('itoolkit', ['itoolkit/README']),
        ('itoolkit', ['itoolkit/LICENSE']),
        ('itoolkit/doc', ['itoolkit/doc/README']),
        ('itoolkit/test', ['itoolkit/test/README']),
        ('itoolkit/sample', ['itoolkit/sample/README']),
    ],
    ext_modules=[
        Extension('itoolkit/itoollib', ['itoolkit/lib/itoollib.c'])
    ],
)
