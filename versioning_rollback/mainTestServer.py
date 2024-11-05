import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
# main server importing all grpc created api functions here
from rollbackCompareApi import version_control_pb2, version_control_pb2_grpc, rollbackCompareServer
from listDeleteApi import list_delete_pb2, list_delete_pb2_grpc, listDeleteServer
from getAndSetVersionApi import function_version_pb2, function_version_pb2_grpc, getAndSetVersionServer
from createGetApi import create_get_version_pb2,create_get_version_pb2_grpc, createGetServer
from archiveRestoreApi import archive_restore_pb2_grpc, archive_restore_pb2, archiveRestoreServer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    version_control_pb2_grpc.add_VersionControlServiceServicer_to_server(rollbackCompareServer.VersionControlService(), server)
    list_delete_pb2_grpc.add_listDeleteServicer_to_server(listDeleteServer.listDeleteServicer(), server)
    function_version_pb2_grpc.add_FunctionVersionServiceServicer_to_server(getAndSetVersionServer.FunctionVersionService(), server)
    create_get_version_pb2_grpc.add_CreateGetServicerServicer_to_server(createGetServer.CreateGetServicerServicer(), server)
    archive_restore_pb2_grpc.add_ArchiveRestoreServiceServicer_to_server(archiveRestoreServer.ArchiveRestoreServiceServicer(), server)

    # Enable reflection for grpcui
    SERVICE_NAMES = (
        version_control_pb2.DESCRIPTOR.services_by_name['VersionControlService'].full_name,
        list_delete_pb2.DESCRIPTOR.services_by_name["listDelete"].full_name,
        function_version_pb2.DESCRIPTOR.services_by_name["FunctionVersionService"].full_name,
        create_get_version_pb2.DESCRIPTOR.services_by_name["CreateGetServicer"].full_name,
        archive_restore_pb2.DESCRIPTOR.services_by_name["ArchiveRestoreService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()