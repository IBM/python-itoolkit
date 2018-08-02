from setuptools import setup, find_packages
from distutils.core import Extension
from distutils.command.build_ext import build_ext
from distutils.command.build_py import build_py

disable_libcall = False

class itoolkit_build_ext(build_ext):
    user_options = build_ext.user_options + [
        ('disable-libcall', None, 'Disable support for iLibCall'),
        ]
    
    def initialize_options(self):
        self.disable_libcall = False
        build_ext.initialize_options(self)
    
    def finalize_options(self):
        build_ext.finalize_options(self)
        
        global disable_libcall
        disable_libcall = self.disable_libcall
        
        # If the user doesn't want libcall, don't build it
        if self.disable_libcall:
            del self.extensions[:]

class itoolkit_build_py(build_py):
    def finalize_options(self):
        build_py.finalize_options(self)
        
        # If the user doesn't want libcall, don't ship the package
        if disable_libcall:
            self.packages.remove('itoolkit.lib')
          
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
  cmdclass={"build_ext": itoolkit_build_ext, 'build_py': itoolkit_build_py},
  packages=find_packages(),
  data_files = [ ('itoolkit', ['itoolkit/README']),
                 ('itoolkit', ['itoolkit/LICENSE']), 
                 ('itoolkit/doc', ['itoolkit/doc/README']), 
                 ('itoolkit/test', ['itoolkit/test/README']), 
                 ('itoolkit/sample', ['itoolkit/sample/README']), 
               ],
  ext_modules=[Extension('itoolkit/itoollib', ['itoolkit/lib/itoollib.c'])],
)

