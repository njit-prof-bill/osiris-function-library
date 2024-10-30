import grpc
from concurrent import futures
import list_delete_pb2
import list_delete_pb2_grpc
from testData import testData

# temporary test server until core-management team implements shared server

class listDeleteServicer(list_delete_pb2_grpc.listDeleteServicer):
    #api 3
    def listFunctionVersions(self, request, context):
        function_name = request.function_name
        #filter from test data functions that match name
        function_info = [function for function in testData if function["function_name"] == function_name]
        # TODO: check for if name does not exist
        response = list_delete_pb2.functionListVersionsResponse()
        for version in function_info:
            version_info = list_delete_pb2.functionVersionsInfo(
                version=version["version"], created_at=version["created_at"]
            )
            response.versioninfo.append(version_info)
        return response
    #api 8
    # def deleteFunction(self, request, context):

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    list_delete_pb2_grpc.add_listDeleteServicer_to_server(listDeleteServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()