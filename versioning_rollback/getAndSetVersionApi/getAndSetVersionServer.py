import grpc
from concurrent import futures
from . import function_version_pb2_grpc, function_version_pb2

# Assuming existing code for version management is here
# For example:
current_version = "1.0.0"  # Placeholder for the current active function version

class FunctionVersionService(function_version_pb2_grpc.FunctionVersionServiceServicer):
    def GetActiveFunctionVersion(self, request, context):
        response = function_version_pb2.GetVersionResponse()
        response.version = current_version
        return response

    def SetActiveFunctionVersion(self, request, context):
        global current_version
        function = request.function
        current_version = request.version
        return function_version_pb2.SetVersionResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    function_version_pb2_grpc.add_FunctionVersionServiceServicer_to_server(FunctionVersionService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()