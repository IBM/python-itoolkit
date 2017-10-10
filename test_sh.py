#!/usr/bin/env python3
from itoolkit import *

from config import transport

from pprint import pprint

toolkit = transport.toolkit()

toolkit.append('asdf', ShellCall('ps -e'))

#toolkit.enable_tracing()

toolkit.execute()

print(toolkit.xml_out())
pprint(toolkit['asdf'].succeeded())
pprint(toolkit['asdf'].data())
pprint(toolkit['asdf'].error_info())
