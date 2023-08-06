#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Queue
import logging

INIT_PROCESS = False
_KEEP_STREAM_THREAD = True  # Should only be changed in test code!
LOG_QUEUE = Queue()
SOURCETYPE = '_json'

LOGGER = logging.getLogger('splunk-log-handler')
LOGGER.setLevel(logging.INFO)

LOGGING_FIELDS = ['created', 'module', 'levelname', 'lineno', 'msg', 'name']
