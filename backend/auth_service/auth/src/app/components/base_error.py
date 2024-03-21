import grpc


class ServiceError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnavailableException(Exception):
    status = grpc.StatusCode.UNAVAILABLE
    code = grpc.StatusCode.UNAVAILABLE
