import grpc
from concurrent import futures
import function_versioning_pb2
import function_versioning_pb2_grpc

# Store functions and their versions
functions_db = {}

class FunctionVersioningServicer(function_versioning_pb2_grpc.FunctionVersioningServicer):
    def CreateFunctionVersion(self, request, context):
        function_name = request.function_name
        code = request.code
        version = request.version

        # Check if the function name and version already exist
        if function_name in functions_db and version in functions_db[function_name]:
            return function_versioning_pb2.CreateFunctionResponse(success=False)
        
        # Initialize function entry if it doesn't exist
        if function_name not in functions_db:
            functions_db[function_name] = {}
        
        # Save the new version
        functions_db[function_name][version] = {
            "code": code,
            "runtime": "Python 3.8"  # Assuming a default runtime for simplicity
        }
        return function_versioning_pb2.CreateFunctionResponse(success=True)
    
    def GetFunctionVersionDetails(self, request, context):
        function_name = request.function_name
        version = request.version

        # Check if the function and version exist
        if function_name in functions_db and version in functions_db[function_name]:
            function_data = functions_db[function_name][version]
            return function_versioning_pb2.GetFunctionDetailsResponse(
                function_name=function_name,
                code=function_data["code"],
                runtime=function_data["runtime"],
                version=version
            )
        # If not found, return an empty response
        return function_versioning_pb2.GetFunctionDetailsResponse()

# Start the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    function_versioning_pb2_grpc.add_FunctionVersioningServicer_to_server(FunctionVersioningServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
