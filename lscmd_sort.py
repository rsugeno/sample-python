#!/usr/bin/env python3

import subprocess
import datetime

result = subprocess.run(["ls", "-l", "--time-style=long-iso", "."], capture_output=True, text=True, check=True)
ls_outputs = result.stdout.split("\n")[1:-1]
ls_outputs.sort(key=lambda x: datetime.datetime.strptime(f"{x.split()[5]} {x.split()[6]}", "%Y-%m-%d %H:%M").timestamp())
for line in ls_outputs:
    print(line)
