#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import json
from logging.handlers import SocketHandler, DatagramHandler

try:
    from queue import Empty as EmptyException
except ImportError:
    from Queue import Empty as EmptyException
import time
import socket
import threading
from datetime import datetime
try:
    import consts
except ImportError:
    import splunk_log_handler.consts as consts

_LOGGERS = {}
_HOSTNAME = socket.gethostname()


def init_splunk_log_handler(service, index, source):
    consts.INIT_PROCESS = True
    is_main_thread_active = lambda: any((i.name == "MainThread") and i.is_alive() for i in threading.enumerate())

    def _handle_logs():
        _count = 0
        while consts._KEEP_STREAM_THREAD:
            try:
                raw = consts.LOG_QUEUE.get_nowait()
            except EmptyException:
                if not is_main_thread_active():
                    service.flush_cache(index, source=source, sourcetype=consts.SOURCETYPE, host=_HOSTNAME,
                                        host_regex=None)
                    break
                else:
                    time.sleep(1)
                    _count += 1
                    continue

            service.cache_event(raw, index, source=source, sourcetype=consts.SOURCETYPE, host=_HOSTNAME, host_regex=None)
            # Flush the cache evey 60 seconds
            if _count >= 60:
                _count = 0
                service.flush_cache(index, source=source, sourcetype=consts.SOURCETYPE, host=_HOSTNAME, host_regex=None)

        service.flush_cache(index, source=source, sourcetype=consts.SOURCETYPE, host=_HOSTNAME, host_regex=None)

    t = threading.Thread(target=_handle_logs)
    t.start()
    return t


class SplunkStreamHandler(logging.Handler):
    def __init__(self, splunk_uri, username, password, index='main', source=None, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self._formatter = logging.Formatter()
        self._threshold = 10
        self._splunk_uri = splunk_uri
        self._username = username
        self._password = password
        self._index = index
        self._source = source or datetime.now()
        self._start_process()

    def _start_process(self):
        if not consts.INIT_PROCESS:
            from .splunk import SplunkStreamService
            service = SplunkStreamService(self._splunk_uri, self._username, self._password)
            self._thread = init_splunk_log_handler(service, self._index, self._source)
            consts.LOGGER.addHandler(self)

    def emit(self, record):
        event_string = self._extract_event(record)
        consts.LOG_QUEUE.put(event_string)

    def _extract_event(self, record):
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.msg = '\n' + self._formatter.formatException(
                    record.exc_info)  # Must use `try..except..` to log the exception info.

        fields = list(consts.LOGGING_FIELDS)
        d = {}
        for i in fields:
            d[i] = getattr(record, i)

        return json.dumps(d)


class SplunkTcpHandler(SocketHandler):
    def __init__(self, host, port, signature=None):
        """
        :param host: splunk hostname or ip
        :param port: splunk received TCP port
        :param signature: a string, will append to each log event if provided.
        It is useful when different program sending to the same splunk tcp port, so you can use different extra_field
        to distinguish them.
        """
        super(SplunkTcpHandler, self).__init__(host, port)
        self._formatter = logging.Formatter()
        self._signature = signature

    def makePickle(self, record):
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.msg = self._formatter.formatException(
                    record.exc_info)

        fields = list(consts.LOGGING_FIELDS)
        d = {'signature': self._signature} if self._signature else {}
        for i in fields:
            d[i] = getattr(record, i)
        # fixme: this is a work around, should dig out why json dumps fails when some exception happens
        try:
            result = (json.dumps(d) + '\n').encode('utf-8')
        except BaseException as e:
            result = str(e)
        return result


class SplunkUdpHandler(DatagramHandler, SplunkTcpHandler):
    def __init__(self, host, port, signature=None):
        SplunkTcpHandler.__init__(self, host, port, signature)
        DatagramHandler.__init__(self, host, port)


class SplunkHecHandler(SplunkStreamHandler):
    def __init__(self, splunk_uri, token, index='main', source=None, level=logging.NOTSET):
        self._token = token
        SplunkStreamHandler.__init__(self, splunk_uri, None, None, index, source, level)

    def _start_process(self):
        if not consts.INIT_PROCESS:
            from .splunk import SplunkHecService
            service = SplunkHecService(self._splunk_uri, self._token)
            self._thread = init_splunk_log_handler(service, self._index, self._source)
            consts.LOGGER.addHandler(self)
