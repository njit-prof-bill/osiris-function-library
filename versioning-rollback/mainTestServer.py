import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
# main server importing all grpc created api functions here
from rollbackCompareApi import version_control_pb2, version_control_pb2_grpc, rollbackCompareServer
from listDeleteApi import list_delete_pb2, list_delete_pb2_grpc, listDeleteServer
from getAndSetVersionApi import function_version_pb2, function_version_pb2_grpc, getAndSetVersionServer
from createGetApi import function_versioning_pb2, function_versioning_pb2_grpc, createGetServer
from archiveRestoreApi import function_service_pb2, function_service_pb2_grpc, archiveRestoreServer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    version_control_pb2_grpc.add_VersionControlServiceServicer_to_server(rollbackCompareServer.VersionControlService(), server)
    list_delete_pb2_grpc.add_listDeleteServicer_to_server(listDeleteServer.listDeleteServicer(), server)
    function_version_pb2_grpc.add_FunctionVersionServiceServicer_to_server(getAndSetVersionServer.FunctionVersionService(), server)
    function_versioning_pb2_grpc.add_FunctionVersioningServicer_to_server(createGetServer.FunctionVersioningServicer(), server)
    function_service_pb2_grpc.add_FunctionServiceServicer_to_server(archiveRestoreServer.FunctionServiceServicer(), server)

    # Enable reflection for grpcui
    SERVICE_NAMES = (
        version_control_pb2.DESCRIPTOR.services_by_name['VersionControlService'].full_name,
        list_delete_pb2.DESCRIPTOR.services_by_name["listDelete"].full_name,
        function_version_pb2.DESCRIPTOR.services_by_name["FunctionVersionService"].full_name,
        function_versioning_pb2.DESCRIPTOR.services_by_name["FunctionVersioning"].full_name,
        function_service_pb2.DESCRIPTOR.services_by_name["FunctionService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()