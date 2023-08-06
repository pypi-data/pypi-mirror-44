import logging
import mock

from oxomo import handlers


class TestHTTPSHandler:
    def setup_class(self):
        self.worker_thread = mock.Mock()
        self.worker_thread.stopped.return_value = True

        self.handler = handlers.HTTPSHandler(
            'url', localname='localname', thread=self.worker_thread)

        self.record = mock.Mock()
        self.record.levelno = logging.DEBUG
        self.record.exc_info = ['one', 'two']
        self.record.message = 'message'
        self.record.created = 'created'
        self.record.name = 'record'

        self.record.getMessage.return_value = self.record.message

        # expected loggly message
        self.expected = {
            'host': 'localname',
            'message': 'message',
            'full_message': 'test',
            'timestamp': 'created',
            'level': 'DEBUG',
            'facility': 'record'
        }

    def test_handler_init(self):
        """ it should create a configured handler """
        h = handlers.HTTPSHandler(
            'url',
            fqdn='fq',
            localname='bob',
            facility='auth',
            thread=self.worker_thread)

        assert h.url == 'url'
        assert h.fqdn == 'fq'
        assert h.localname == 'bob'
        assert h.facility == 'auth'

    def test_get_full_message_msg(self):
        """ it should log the message """
        self.record.exc_info = None
        result = self.handler.get_full_message(self.record)

        assert 'message' == result

    @mock.patch('traceback.format_exception')
    def test_get_full_message_exc(self, trace):
        """ it should log the traceback """
        self.record.exc_info = trace.return_value = ['trace', 'two']

        result = self.handler.get_full_message(self.record)

        assert 'trace\ntwo' == result
