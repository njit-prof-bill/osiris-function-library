import grpc
from concurrent import futures
import version_control_pb2
import version_control_pb2_grpc


sampleData = {
    "addNumbers": [
        {"version": "1.0", "code": "def addNumbers(a, b):\n    return a + b"},
        {"version": "2.0", "code": "def addNumbers(a, b):x`\n    return a - b"}
    ]
}

class VersionControlService(version_control_pb2_grpc.VersionControlServiceServicer):
    def rollbackToPreviousVersion(self, request, context):
        pass

    def compareFunctionVersions(self, request, context):
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    version_control_pb2_grpc.add_VersionControlServiceServicer_to_server(VersionControlService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
