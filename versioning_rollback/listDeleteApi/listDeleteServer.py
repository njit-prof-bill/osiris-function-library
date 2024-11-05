import grpc
from grpc_reflection.v1alpha import reflection
from concurrent import futures
from . import list_delete_pb2, list_delete_pb2_grpc
# data to test with
testData = [
  {"function_name": "addNumbers","code":"def add(a, b): return a + b", "version":"1.0", "created_at": "2024-10-01"},
  {"function_name": "addNumbers","code":"def add(a, b, c): return a + b + c", "version":"2.0", "created_at": "2024-10-20"},
  {"function_name": "testFunc","code":"def test(str): return str", "version":"1.0", "created_at": "2024-9-01"},
  {"function_name": "testFunc","code":"def test(str): return 'Your string is '+str", "version":"2.0", "created_at": "2024-10-01"},
  {"function_name": "testFunc","code":"def test(str1, str2): return 'Your strings are '+str1+' and '+str2", "version":"3.0", "created_at": "2024-10-28"},
]

class listDeleteServicer(list_delete_pb2_grpc.listDeleteServicer):
    #api 3
    def listFunctionVersions(self, request, context):
        functionName = request.functionName
        #filter from test data functions that match name
        functionInfo = [function for function in testData if function["function_name"] == functionName]
        response = list_delete_pb2.functionListVersionsResponse()
        for version in functionInfo:
            versionInfo = list_delete_pb2.functionVersionsInfo(
                version=version["version"], createdAt=version["created_at"]
            )
            response.versioninfo.append(versionInfo)
        return response
    
    #api 8
    def deleteFunction(self, request, context):
        global testData # to modify testData

        functionName = request.functionName
        version = request.version
        # checking if function to delete exists
        filteredFunctions= [function for function in testData if function["function_name"] == functionName and function['version'] == version]
        response = list_delete_pb2.deleteFunctionResponse()
        if len(filteredFunctions) == 1:
            #function to delete exists so remove from database and return true
            testData= [function for function in testData if not (function["function_name"] == functionName and function['version'] == version)]
            response.deleteBool = True
        else:
            response.deleteBool = False
        return response
        
# temporary test server until core-management team implements shared server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    list_delete_pb2_grpc.add_listDeleteServicer_to_server(listDeleteServicer(), server)

    # need to have reflection to use grpcurl or grpcui
    SERVICE_NAMES = (
        list_delete_pb2.DESCRIPTOR.services_by_name["listDelete"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()