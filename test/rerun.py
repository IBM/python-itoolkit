import sys
import unittest

if sys.version_info < (2,7):
  # 2.6 user, you may need ...
  # easy_install discover
  from discover import DiscoveringTestLoader
  test_loader = DiscoveringTestLoader()
  all_tests = test_loader.discover(".", pattern="test_*.py")
else:
  all_tests = unittest.TestLoader().discover(".",pattern='test_*.py')

unittest.TextTestRunner().run(all_tests)


