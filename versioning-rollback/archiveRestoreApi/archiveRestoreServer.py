from concurrent import futures
import grpc
from archiveRestoreApi import function_service_pb2, function_service_pb2_grpc, restoreArchivedVersion, archiveFunctionVersion

functions = {}

functions['example_function'] = {
    'v1.0': 'active',
    'v1.1': 'archived'
}

class FunctionServiceServicer(function_service_pb2_grpc.FunctionServiceServicer):
    def ArchiveFunctionVersion(self, request, context):
        success = archiveFunctionVersion.archiveFunctionVersion(request.function_name, request.version)
        message = "Archived successfully." if success else "Failed to archive."
        return function_service_pb2.FunctionResponse(success=success, message=message)

    def RestoreArchivedVersion(self, request, context):
        success = restoreArchivedVersion.restoreArchivedVersion(request.function_name, request.version)
        message = "Restored successfully." if success else "Failed to restore."
        return function_service_pb2.FunctionResponse(success=success, message=message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    function_service_pb2_grpc.add_FunctionServiceServicer_to_server(FunctionServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

