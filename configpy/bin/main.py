#!/usr/bin/env python3
"""Usage:
./main.py config.py
./main.py config
"""

import importlib
import re
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <CONFIG MODULE>")

sys.path.append("../etc")

match = re.fullmatch(r"^(.*)\.py$", sys.argv[1])
if match:
    module_name = match.group(1)
else:
    module_name = sys.argv[1]
config = importlib.import_module(module_name)

print(config.SERVER)
print(config.PASSWORD)
