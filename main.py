import grpc
from concurrent import futures
from core_management import core_management_pb2
from core_management import core_management_pb2_grpc
from core_management.server import util
from core_management.server.data_store import function_library

class CoreManagementServicer(core_management_pb2_grpc.CoreManagementServicer):
    def AddFunction(self, request, context):
        success, message = util.addFunctionToLibrary(request.function_name, request.code, request.runtime_env, request.version)
        return core_management_pb2.AddFunctionResponse(success=success, message=message)
    
    def PublishFunction(self, request, context):
        success = util.publishFunction(request.function_name)
        message = f"Function {request.function_name} published successfully." if success else f"Failed to publish function {request.function_name}."
        return core_management_pb2.PublishFunctionResponse(success=success, message=message)
    
    def UnpublishFunction(self, request, context):
        success = util.unpublishFunction(request.function_name)
        message = f"Function {request.function_name} unpublished successfully." if success else f"Failed to unpublish function {request.function_name}."
        return core_management_pb2.PublishFunctionResponse(success=success, message=message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    core_management_pb2_grpc.add_CoreManagementServicer_to_server(CoreManagementServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
