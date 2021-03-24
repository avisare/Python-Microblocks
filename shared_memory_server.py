from transportation_protocols.connection_factory import ConnectionFactory
from pypsexec_client.messages import Request, Response
import SharedMemoryWrapper


class SharedMemoryServer:
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

    def start_server(self, configurations):
        server_client_connection = ConnectionFactory.get_connection(*configurations)
        self._handle_client(server_client_connection)

    def _handle_client(self, connection):
        try:
            while True:
                client_request = connection.receive()
                if client_request and self._is_valid_request(client_request):
                    if client_request.request_code == self.EXIT:
                        return
                    response = self._smt_functions.get(client_request.request_code, None)[1](client_request.arguments)
                    connection.send(response)
                else:
                    error_response = Response(self.ERROR)
                    connection.send(error_response)

        except ConnectionResetError:
            print("Client close connection, server is down")
            return

    def _is_valid_request(self, request):
        if isinstance(request, Request) and isinstance(request.request_code, int):
            if self.SMT_INIT <= request.request_code <= self.SMT_CLEAR_HISTORY:
                return self._is_valid_arguments(request)
            return request.request_code == self.EXIT
        return False

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
        return not isinstance(arguments[0], int) and not isinstance(arguments[0], str) and isinstance(arguments[1], str)

    def _check_smt_get_by_counter(self, arguments):
        if isinstance(arguments, tuple) and (len(arguments) == 4 or len(arguments) == 5) and not isinstance(arguments[0], int) and not isinstance(arguments[0], str):
            return isinstance(arguments[1], int) and isinstance(arguments[2], int) and isinstance(arguments[3], str)
        return False

    def _check_smt_get_latest(self, arguments):
        if isinstance(arguments, tuple) and (len(arguments) == 2 or len(arguments) == 3):
            return not isinstance(arguments[0], str) and not isinstance(arguments[0], int) and isinstance(arguments[1], str)
        return False

    def _check_smt_get_oldest(self, arguments):
        if isinstance(arguments, tuple) and (len(arguments) == 2 or len(arguments) == 3):
            return not isinstance(arguments[0], str) and not isinstance(arguments[0], int) and isinstance(arguments[1], str)
        return False

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
        return eval(f"Response(SharedMemoryWrapper.{arguments[1]}().publish(arguments))")

    def _smt_get_by_counter(self, arguments):
        if len(arguments) == 4:
            topic_name = arguments[2]
            arguments = arguments[:2] + [arguments[-1]]
            return eval(f"Response(SharedMemoryWrapper.{topic_name}().getByCounter(*arguments), (arguments[0], arguments[-1]))")
        return eval(f"Response(SharedMemoryWrapper.{arguments[-1]}().getByCounter(*arguments[:-1]), arguments[0])")

    def _smt_get_latest(self, arguments):
        if len(arguments) == 3:
            topic_name = arguments[1]
            arguments = [arguments[0], arguments[-1]]
            return eval(f"Response(SharedMemoryWrapper.{topic_name}().getLatest(*arguments), (arguments[0], arguments[1]))")
        return eval(f"Response(SharedMemoryWrapper.{arguments[-1]}().getLatest(arguments[1]), arguments)")

    def _smt_get_oldest(self, arguments):
        if len(arguments) == 3:
            topic_name = arguments[1]
            arguments = [arguments[0], arguments[-1]]
            return eval(f"Response(SharedMemoryWrapper.{topic_name}().getOldest(*arguments), (arguments[0], arguments[1]))")
        return eval(f"Response(SharedMemoryWrapper.{arguments[-1]}().getOldest(arguments[1]), arguments)")

    def _smt_get_publish_count(self, arguments):
        return Response(True, SharedMemoryWrapper.SMT_GetPublishCount(arguments))

    def _smt_clear_history(self, arguments):
        return Response(SharedMemoryWrapper.SMT_ClearHistory(arguments))
