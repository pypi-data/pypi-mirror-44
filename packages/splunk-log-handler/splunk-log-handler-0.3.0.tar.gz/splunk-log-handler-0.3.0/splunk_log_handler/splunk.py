#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import Queue
except ImportError:
    import queue as Queue
import json
import logging
from xml.etree import ElementTree
import requests
from collections import defaultdict
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout
from .consts import LOGGER

requests.packages.urllib3.disable_warnings()
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
# All handlers in different threads share the same session.
_SESSION = requests.Session()
_SESSION.mount('https', HTTPAdapter(pool_connections=20, pool_maxsize=10))


class SplunkRestService(object):
    def __init__(self, splunk_uri, credential):
        """
        :param splunk_uri: Specify the splunk as servername:mgmt_port or URI:mgmt_port
        :param credential: can be tuple of `username, password`, or just a token string
        """
        self._init_logger()
        self.splunk_uri = splunk_uri
        if isinstance(credential, str):
            self._splunk_header = {'Authorization': 'Splunk %s' % credential}
        else:
            self.username, self.password = credential
            self._splunk_header = {'Authorization': 'Splunk %s' % self._password2sessionkey()}

    def _init_logger(self):
        self.logger = LOGGER

    def _password2sessionkey(self):
        """
        Get a session key from the auth system
        """
        uri = self.splunk_uri + '/services/auth/login'
        body = {'username': self.username, 'password': self.password}
        response = _SESSION.post(uri, data=body, verify=False, timeout=30)

        if response.status_code != 200:
            self.logger.error('Cannot get session key from `{0}`'.format(self.splunk_uri))
            raise Exception('Cannot get session key from `{0}`'.format(self.splunk_uri))

        root = ElementTree.fromstring(response.content)
        session_key = root.findtext('sessionKey')

        return session_key

    def _update_splunk_header(self):
        self._splunk_header = {'Authorization': 'Splunk %s' % self._password2sessionkey()}

    def request_get(self, endpoint, timeout=30, try_again=True):
        assert endpoint.startswith('/')
        uri = self.splunk_uri + endpoint
        try:
            response = _SESSION.get(uri, headers=self._splunk_header, params={'output_mode': 'json'}, verify=False,
                                    timeout=timeout)
        except Timeout as e:
            self.logger.error('HTTP read timeout at `{0}`'.format(self.splunk_uri + '/' + endpoint))
            raise Exception('ReadTimeout', e)

        # If the session key is not correct.
        if 401 == response.status_code and try_again:
            self._update_splunk_header()
            response = self.request_get(endpoint, timeout, False)

        parsed_response = response.json()
        if response.status_code == 200:
            return parsed_response
        else:
            self.logger.error(
                'HTTP status code is {0} at `{1}`'.format(response.status_code, self.splunk_uri + '/' + endpoint))
            raise Exception('Response', response)

    def request_post(self, endpoint, data, params=None, extra_header=None, try_again=True):
        """
        :param endpoint: the rest endpoint.
        :param data: the data to post.
        :param extra_header: a dict contains header info.
        :param try_again: will try to post again if failed due to incorrect session key.
        """
        assert endpoint.startswith('/')
        headers = self._splunk_header
        if extra_header:
            headers.update(extra_header)
        uri = self.splunk_uri + endpoint
        try:
            response = _SESSION.post(uri, headers=headers, data=data, params=params, verify=False)
        except AttributeError:
            # The process goes here only when it is going to terminate and _SESSION is destroyed.
            response = requests.post(uri, headers=headers, data=data, params=params, verify=False)

        # If the session key is not correct.
        if 401 == response.status_code and try_again:
            self._update_splunk_header()
            response = self.request_post(endpoint, data, params, extra_header, False)

        return response


class SplunkOutputService(SplunkRestService):
    """
    Used to output events into a splunk.
    By default, post the events every 60 seconds with no speed limit.
    """

    def __init__(self, splunk_uri, credential, post_endpoint, flush_hook=None):
        SplunkRestService.__init__(self, splunk_uri, credential)
        self._cache_event = defaultdict(lambda: '')  # A dict with sourcetype as key, send content as value.
        self._cache_events_number = defaultdict(lambda: 0)
        self._queue = Queue.Queue(maxsize=10000)
        self.flush_hook = flush_hook
        self._post_endpoint = post_endpoint

    def cache_event(self, event, index, source, sourcetype, host, host_regex):
        self._cache_event[(index, source, sourcetype, host, host_regex)] += event.strip() + '\n'

    def flush_all_cache(self):
        for signature in self._cache_event:
            self.flush_cache(*signature)

    def flush_cache(self, index, source, sourcetype, host, host_regex):
        if self.flush_hook:
            self.flush_hook()
        # Will flush all events if sourcetype not specified.
        if sourcetype is None:
            self.flush_all_cache()
        else:
            try:
                if self._cache_event[(index, source, sourcetype, host, host_regex)]:
                    response = self.request_post(self._post_endpoint,
                                                 data=self._cache_event[(index, source, sourcetype, host, host_regex)],
                                                 params={'index': index, 'source': source,
                                                         'sourcetype': sourcetype, 'host': host,
                                                         'host_regex': host_regex})
                    if response.status_code >= 400:
                        self.logger.error(
                            'Flush events into splunk({0}) failed: {1}'.format(self.splunk_uri, response.text))
                    else:
                        self.logger.debug(
                            'Flushed data to {}. index:{},source:{},sourcetype:{},host:{}'.format(
                                self.splunk_uri,
                                index,
                                source,
                                sourcetype,
                                host,
                            ))
                    self._cache_event[(index, source, sourcetype, host, host_regex)] = ''  # Release the cache.
            except BaseException as e:
                self.logger.error('Error occurs when sending events into splunk.', exc_info=True)


class SplunkStreamService(SplunkOutputService):
    def __init__(self, splunk_uri, username, password, flush_hook=None):
        super(SplunkStreamService, self).__init__(splunk_uri, (username, password),
                                                  post_endpoint='/services/receivers/stream', flush_hook=flush_hook)
        self._splunk_header['x-splunk-input-mode'] = 'streaming'


class SplunkHecService(SplunkOutputService):
    def __init__(self, splunk_uri, token, flush_hook=None):
        super(SplunkHecService, self).__init__(splunk_uri, token,
                                               post_endpoint='/services/collector/event', flush_hook=flush_hook)

    def cache_event(self, event, index, source, sourcetype, host, host_regex):
        # event_string = event.encode('utf-8')
        self._cache_event[(index, source, sourcetype, host, host_regex)] += json.dumps(
            {"event": event.strip()})
