#!/usr/bin/env python3
# Return 1 if minute is odd, 0 if minute is even.
# PYTHON_PREAMBLE_START_COPYRIGHT:{{{
# Christopher David Cotton (c)
# http://www.cdcotton.com
# PYTHON_PREAMBLE_END:}}}

import datetime

isodd = datetime.datetime.now().minute % 2
print(isodd)
