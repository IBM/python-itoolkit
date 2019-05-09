from setuptools import setup, find_packages, Extension


setup(
    name='itoolkit',
    version='1.6.0',
    description='IBM i XMLSERVICE toolkit for Python',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/litmis/python-itoolkit',
    author="IBM",
    license='MIT',
    zip_safe=False,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=[
        Extension('itoolkit/transport/_direct',
                  ['src/itoolkit/transport/direct.c'])
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
