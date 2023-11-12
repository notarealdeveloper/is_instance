#!/usr/bin/env python3

import sys
from .main import is_instance
import callable_module

old = sys.modules[__name__]
new = callable_module.from_module(is_instance, old)
sys.modules[__name__] = new
