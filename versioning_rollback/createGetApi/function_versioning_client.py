import grpc
from createGetApi import create_get_version_pb2, create_get_version_pb2_grpc

def run():
    # Connect to the server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = create_get_version_pb2_grpc.FunctionVersioningStub(channel)
        
        # Test CreateFunctionVersion
        create_response = stub.CreateFunctionVersion(
            create_get_version_pb2.CreateFunctionRequest(
                function_name="addNumbers",
                code="def add(a, b): return a + b",
                version="2.0"
            )
        )
        print("CreateFunctionVersion response:", create_response.success)
        
        # Test GetFunctionVersionDetails
        details_response = stub.GetFunctionVersionDetails(
            create_get_version_pb2.GetFunctionDetailsRequest(
                function_name="addNumbers",
                version="2.0"
            )
        )
        print("GetFunctionVersionDetails response:")
        print("Function Name:", details_response.function_name)
        print("Code:", details_response.code)
        print("Runtime:", details_response.runtime)
        print("Version:", details_response.version)

if __name__ == '__main__':
    run()
