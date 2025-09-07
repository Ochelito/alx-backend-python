#!/usr/bin/python3
import sys
import importlib
processing = importlib.import_module('1-batch_processing')

##### print processed users in a batch of 50
try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()