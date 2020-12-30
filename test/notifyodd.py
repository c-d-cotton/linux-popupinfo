#!/usr/bin/env python3
# print a popup when you run this script if the last time this was run (or it has not been run since shutting down) the minute was even and the current minute is odd.
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/../')

sys.path.append(str(__projectdir__))
from displaypopup_func import genpopup_test
genpopup_test('The current minute is odd. The last time this code was run, the minute was not odd.', title = 'Minute Details', test = __projectdir__ / Path('test/isoddmin.py'), savefile = '/tmp/oddminutetest.txt', testnewlytrue = True, shellinput_test = True)
