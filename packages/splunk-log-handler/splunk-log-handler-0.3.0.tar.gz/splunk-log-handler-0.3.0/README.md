> Output logs to a splunk automatically by **splunk-log-handler**

## Feature

- Support sending logs to remote splunk via multiple ways:
  - Streaming
  - Tcp
  - Udp
  - HEC
- Realtime processing
- Sending events asynchronously, will not block main process
- JSON format
- Support multi-thread/multi-process
- Python2 and Python3 are supported

## Installation

Use pip:

```bash
pip install splunk-log-handler -i https://repo.splunk.com/artifactory/api/pypi/pypi-virtual/simple
```

## User guide

### Splunk Stream Handler

With splunk stream handler, you can specify the target index and source of remote splunk:

```python
from splunk_log_handler import SplunkStreamHandler
import logging

handler = SplunkStreamHandler('https://my-splunk-host:8089', 'admin', 'password', index='main', source='testing', level=logging.INFO)
logger = logging.getLogger('demo')
logger.addHandler(handler)
logger.info('This log will be sent to a splunk.')
```

#### Limition

1. For now the splunk stream handler is limited to send logs to one splunk, i.e. you shuld not initialize multiple `SplunkStreamHandler` instances in your code. (If multiple handlers are initilized, only the first handler's configuration will take effect!)

   > *If you really want to send logs to different splunk servers, I suggest you to send to a splunk forwarder and configure that forwarder to distribute the logs to multiple splunks.*

2. We use a individual thread in main process to do the sending tasks, so if the main process is crashed, the logs will no longer be sent out.

   > Maybe in the future, we will support to use a individual process to do the logging things and thus can avoid such problem.

### Splunk Tcp Handler

If you can accept duplicate logs, splunk tcp handler will be a good choice. It is cheaper (in perf scope) than splunk stream handler and it will not expose your username and password of remote splunk.

```python
from splunk_log_handler import SplunkTcpHandler
import logging

handler = SplunkTcpHandler('my-splunk-host', 9997)
logger = logging.getLogger('demo')
logger.addHandler(handler)
logger.info('This log will be sent to a splunk.')
```

### Splunk Udp handler

Similar to splunk tcp handler, but send via UDP socket:

```python
from splunk_log_handler import SplunkUdpHandler
import logging

handler = SplunkUdpHandler('my-splunk-host', 9984)
logger = logging.getLogger('demo')
logger.addHandler(handler)
logger.info('This log will be sent to a splunk.')
```

### Splunk HEC Handler

Similar to splunk stream handler (use token instead of username, password, and note that the port in spunk_uri should be the HEC port):

```python
from splunk_log_handler import SplunkHecHandler
import logging

handler = SplunkHecHandler('https://my-splunk-host:8088', 'YOUR-TOKEN-HERE', index='main', source='testing', level=logging.INFO)
logger = logging.getLogger('demo')
logger.addHandler(handler)
logger.info('This log will be sent to a splunk.')
```

