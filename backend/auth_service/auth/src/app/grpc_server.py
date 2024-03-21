from concurrent import futures

import grpc
from components.auth_grpc import Auth
from components.protobufs import auth_grpc_pb2_grpc
from main import app


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_grpc_pb2_grpc.add_AuthServicer_to_server(Auth(app), server)
    server.add_insecure_port("[::]:50055")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
