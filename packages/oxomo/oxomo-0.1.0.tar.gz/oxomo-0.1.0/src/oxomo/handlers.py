import json
import logging
import logging.handlers
from queue import Queue
import urllib.request
import threading
import traceback


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class HTTPSHandler(logging.Handler):

    _max_queue_size = 50

    def __init__(self,
                 url,
                 fqdn=False,
                 localname=None,
                 facility=None,
                 queue=None,
                 thread=None):
        logging.Handler.__init__(self)
        self.url = url
        self.fqdn = fqdn
        self.localname = localname
        self.facility = facility

        self._init_queue(queue)
        self._init_start_thread(thread)

    def _init_queue(self, queue):
        if queue is None:
            self._queue = Queue(self._max_queue_size)
        else:
            self._queue = queue

    def _init_start_thread(self, thread):
        if thread is None:
            self._worker_thread = StoppableThread(target=self._worker)
        else:
            self._worker_thread = thread
        self._worker_thread.start()

    def get_full_message(self, record):
        if record.exc_info:
            return '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            return record.getMessage()

    def emit(self, record):
        try:
            record = self.format(record)
            self._queue.put(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)

    def _http_post(self, record):
        post = self._prepare_post(record)
        req = urllib.request.Request(self.url, **post)
        urllib.request.urlopen(req)

    def _format_payload(self, record):
        return self.format(record)

    def _worker(self):
        while self._worker_thread.stopped() is False:
            item = self._queue.get(True)
            self._http_post(item)
            self._queue.task_done()
            if self._queue.empty() and \
                    (threading.main_thread().is_alive() is False):
                self._worker_thread.stop()


class RocketChatHandler(HTTPSHandler):
    def _prepare_post(self, record):
        return {
            "data": {json.dumps({
                "text": record
            }).encode('utf8')},
            "headers": {
                'content-type': 'application/json'
            }
        }
