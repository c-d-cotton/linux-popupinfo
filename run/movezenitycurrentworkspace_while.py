#!/usr/bin/env python3
"""
I should call this with ./movezenitycurrentworkspace.py &
"""
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/../')

sys.path.append(str(__projectdir__))
from displaypopup_func import movezenitycurrentworkspace_while
movezenitycurrentworkspace_while()
