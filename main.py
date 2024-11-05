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
    
    def UpdateFunction(self, request, context):
        success, message = util.updateFunctionInLibrary(request.function_name, request.code, request.version)
        return core_management_pb2.UpdateFunctionResponse(success=success, message=message)

    def RemoveFunction(self, request, context):
        success, message = util.removeFunctionFromLibrary(request.function_name)
        return core_management_pb2.RemoveFunctionResponse(success=success, message=message)
    
    def ListFunctions(self, request, context):
        success, message = util.listFunctionsInLibrary()
        return core_management_pb2.ListFunctionsResponse(success=success, message=message)

    def GetFunctionDetails(self, request, context):
        success, message = util.getFunctionDetails(request.function_name)
        return core_management_pb2.GetFunctionDetailsResponse(success=success, message=message)

    def PublishFunction(self, request, context):
        success, message = util.publishFunction(request.function_name)
        return core_management_pb2.PublishFunctionResponse(success=success, message=message)
    
    def UnpublishFunction(self, request, context):
        success, message = util.unpublishFunction(request.function_name)
        return core_management_pb2.PublishFunctionResponse(success=success, message=message)
      
    def ArchiveFunction(self, request, context):
        success, message = util.archiveFunction(request.function_name)
        return core_management_pb2.ArchiveFunctionResponse(success=success, message=message)
    def RollbackFunctionVersion(self, request, context):
        success, message = util.rollbackFunctionVersion(request.function_name, request.target_version)
        return core_management_pb2.RollbackFunctionVersionResponse(success=success, message=message)
    def SearchFunctionByRuntime(self, request, context):
        # Call the search function from util
        functions = util.searchFunctionByRuntime(request.runtime)
        return core_management_pb2.SearchFunctionByRuntimeResponse(
            functions=[
                core_management_pb2.FunctionDetails(
                    function_name=func["function_name"],
                    version=func["version"]
                ) for func in functions
            ]
        )
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    core_management_pb2_grpc.add_CoreManagementServicer_to_server(CoreManagementServicer(), server)
    server.add_insecure_port('[::]:1500')
    server.start()
    print("Server is running on port 1500...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
