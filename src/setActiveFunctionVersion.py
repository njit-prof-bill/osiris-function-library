import grpc
import function_version_pb2
import function_version_pb2_grpc

def get_active_function_version():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = function_version_pb2_grpc.FunctionVersionServiceStub(channel)
        response = stub.GetActiveFunctionVersion(function_version_pb2.GetVersionRequest())
        print("Current active function version:", response.version)

def set_active_function_version(version):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = function_version_pb2_grpc.FunctionVersionServiceStub(channel)
        request = function_version_pb2.SetVersionRequest(version=version)
        response = stub.SetActiveFunctionVersion(request)
        print("Version set successfully:", response.success)

if __name__ == '__main__':
    # Example usage
    get_active_function_version()    # Retrieve the current version
    set_active_function_version("2.0.0")  # Set a new version
