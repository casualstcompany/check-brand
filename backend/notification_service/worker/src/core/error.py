import grpc


class UnavailableException(Exception):
    status = grpc.StatusCode.UNAVAILABLE
    code = grpc.StatusCode.UNAVAILABLE
