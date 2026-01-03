# pyfitel
pyfitel is a Python wrapper for [FITELnet API](https://www.furukawaelectric.com/fitelnet/technical/FITELnet_API.html).

## Usage

Install

```
pip install pyfitel
```

Sample Code

```Python
import pyfitel

fitel = pyfitel.FITELnetAPI("192.168.1.1", 50443, "user", "password", tls=False)

# Show command
output = fitel.command("show version")
print(output)

# Configure
config = """
interface Loopback 1
description Foobar
"""
fitel.config(config)
```