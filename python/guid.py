#!/usr/bin/python

import os
import hashlib

random_data = os.urandom(128)
print hashlib.md5(random_data).hexdigest()[:16]
