from threading import Thread
from pickle import loads, dumps
from tcp_communication import TCP_Connection
from messages import Request, Response
import SharedMemoryWrapper


class SharedMemoryServer:
    BUFFER_SIZE = 1024
    ERROR = 0
    SMT_INIT = 1
    SMT_VERSION = 2
    SMT_CREATE_TOPIC = 3
    SMT_PUBLISH = 4
    SMT_GET_BY_COUNTER = 5
    SMT_GET_LATEST = 6
    SMT_GET_OLDEST = 7
    SMT_GET_PUBLISH_COUNT = 8
    SMT_CLEAR_HISTORY = 9
    EXIT = 999

    def __init__(self):
        self._smt_functions = {
            self.SMT_INIT: (self._check_smt_init, self._smt_init),
            self.SMT_VERSION: (self._check_smt_version, self._smt_version),
            self.SMT_CREATE_TOPIC: (self._check_smt_create_topic, self._smt_create_topic),
            self.SMT_PUBLISH: (self._check_smt_publish, self._smt_publish),
            self.SMT_GET_BY_COUNTER: (self._check_smt_get_by_counter, self._smt_get_by_counter),
            self.SMT_GET_LATEST: (self._check_smt_get_latest, self._smt_get_latest),
            self.SMT_GET_OLDEST: (self._check_smt_get_oldest, self._smt_get_oldest),
            self.SMT_GET_PUBLISH_COUNT: (self._check_smt_get_publish_count, self._smt_get_publish_count),
            self.SMT_CLEAR_HISTORY: (self._check_smt_clear_history, self._smt_clear_history),
        }

    def start_server(self):
        while True:
            server_client_connection = TCP_Connection(1234, False)
            client_thread = Thread(target=self._handle_client, args=(server_client_connection,))
            client_thread.start()

    def _handle_client(self, connection):
        while True:
            client_request = connection.receive(self.BUFFER_SIZE)
            parsed_request = self._parse_request(client_request)
            if parsed_request and self._is_valid_request(parsed_request):
                if parsed_request.request_code == self.EXIT:
                    return
                response = self._smt_functions.get(parsed_request.request_code, None)[1](parsed_request.arguments)
                connection.send(dumps(response))
            else:
                error_response = Response(self.ERROR)
                connection.send(dumps(error_response))

    def _parse_request(self, client_request):
        try:
            request_object = loads(client_request)
        except TypeError:
            return False
        return request_object

    def _is_valid_request(self, request):
        if isinstance(request, Request) and isinstance(request.request_code, int) \
                and self.SMT_INIT <= request.request_code <= self.SMT_CLEAR_HISTORY:
            return self._is_valid_arguments(request)
        return request.request_code == self.EXIT

    def _is_valid_arguments(self, request):
        code_functions = self._smt_functions.get(request.request_code, None)
        if code_functions is None:
            return False
        return code_functions[0](request.arguments)


    def _check_smt_version(self, arguments):
        return arguments is None

    def _check_smt_init(self, arguments):
        return arguments is None

    def _check_smt_create_topic(self, arguments):
        if isinstance(arguments, tuple) and len(arguments) == 4 \
                and isinstance(arguments[0], str):
            for argument in arguments[1:]:
                if not isinstance(argument, int):
                    return False
            return True
        return False

    def _check_smt_publish(self, arguments):
        return not isinstance(arguments, int) and not isinstance(arguments, str)

    def _check_smt_get_by_counter(self, arguments):
        if isinstance(arguments, list) and (len(arguments) == 3 or len(arguments) == 4) and not isinstance(arguments[0], int) and not isinstance(arguments[0], str):
            return isinstance(arguments[1], int) and isinstance(arguments[2], int)
        return False

    def _check_smt_get_latest(self, arguments):
        return (isinstance(arguments, tuple) and len(arguments) == 2) or not isinstance(arguments, int) and not isinstance(arguments, str)

    def _check_smt_get_oldest(self, arguments):
        return (isinstance(arguments, tuple) and len(arguments) == 2) or not isinstance(arguments, int) and not isinstance(arguments, str)

    def _check_smt_get_publish_count(self, arguments):
        return isinstance(arguments, str)

    def _check_smt_clear_history(self, arguments):
        return isinstance(arguments, str)

    def _smt_version(self, arguments):
        version = SharedMemoryWrapper.SMT_Version()
        response = Response(True, version)
        return response

    def _smt_init(self, arguments):
        return Response(SharedMemoryWrapper.SMT_Init())

    def _smt_create_topic(self, arguments):
        return Response(SharedMemoryWrapper.SMT_CreateTopic(*arguments))

    def _smt_publish(self, arguments):
        return Response(SharedMemoryWrapper.publish(arguments))

    def _smt_get_by_counter(self, arguments):
        if len(arguments) == 4:
            return Response(SharedMemoryWrapper.getByCounter(*arguments), (arguments[0], arguments[3]))
        temp = SharedMemoryWrapper.getByCounter(*arguments)
        return Response(temp, arguments[0])

    def _smt_get_latest(self, arguments):
        if isinstance(arguments, tuple):
            return Response(SharedMemoryWrapper.getLatest(*arguments), (arguments[0], arguments[1]))
        result = SharedMemoryWrapper.getLatest(arguments)
        return Response(result, arguments)

    def _smt_get_oldest(self, arguments):
        if isinstance(arguments, tuple):
            return Response(SharedMemoryWrapper.getOldest(*arguments), (arguments[0], arguments[1]))
        return Response(SharedMemoryWrapper.getOldest(arguments), arguments)

    def _smt_get_publish_count(self, arguments):
        return Response(True, SharedMemoryWrapper.SMT_GetPublishCount(arguments))

    def _smt_clear_history(self, arguments):
        return Response(SharedMemoryWrapper.SMT_ClearHistory(arguments))
