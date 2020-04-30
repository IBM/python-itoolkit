from setuptools import setup, find_packages


setup(
    name='itoolkit',
    version='1.7.0-dev',
    description='IBM i XMLSERVICE toolkit for Python',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/IBM/python-itoolkit',
    author="IBM",
    license='MIT',
    zip_safe=False,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
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
