import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
# versioning rollback api imports
from versioning_rollback.rollbackCompareApi import version_control_pb2, version_control_pb2_grpc, rollbackCompareServer
from versioning_rollback.listDeleteApi import list_delete_pb2, list_delete_pb2_grpc, listDeleteServer
from versioning_rollback.getAndSetVersionApi import function_version_pb2, function_version_pb2_grpc, getAndSetVersionServer
from versioning_rollback.createGetApi import create_get_version_pb2,create_get_version_pb2_grpc, createGetServer
from versioning_rollback.archiveRestoreApi import archive_restore_pb2_grpc, archive_restore_pb2, archiveRestoreServer
# core management api imports
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
    version_control_pb2_grpc.add_VersionControlServiceServicer_to_server(rollbackCompareServer.VersionControlService(), server)
    list_delete_pb2_grpc.add_listDeleteServicer_to_server(listDeleteServer.listDeleteServicer(), server)
    function_version_pb2_grpc.add_FunctionVersionServiceServicer_to_server(getAndSetVersionServer.FunctionVersionService(), server)
    create_get_version_pb2_grpc.add_CreateGetServicerServicer_to_server(createGetServer.CreateGetServicerServicer(), server)
    archive_restore_pb2_grpc.add_ArchiveRestoreServiceServicer_to_server(archiveRestoreServer.ArchiveRestoreServiceServicer(), server)

    # Enable reflection to allow testing using grpcui
    SERVICE_NAMES = (
        version_control_pb2.DESCRIPTOR.services_by_name['VersionControlService'].full_name,
        list_delete_pb2.DESCRIPTOR.services_by_name["listDelete"].full_name,
        function_version_pb2.DESCRIPTOR.services_by_name["FunctionVersionService"].full_name,
        create_get_version_pb2.DESCRIPTOR.services_by_name["CreateGetServicer"].full_name,
        archive_restore_pb2.DESCRIPTOR.services_by_name["ArchiveRestoreService"].full_name,
        core_management_pb2.DESCRIPTOR.services_by_name["CoreManagement"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()