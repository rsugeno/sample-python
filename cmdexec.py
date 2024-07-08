#!/usr/bin/env python3

import subprocess

result = subprocess.run(["ls", "--full-time", "."], capture_output=True, text=True, check=True)

for line in result.stdout.split("\n")[1:-1]:
    print(line)
