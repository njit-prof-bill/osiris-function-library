import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
from . import version_control_pb2,version_control_pb2_grpc

class VersionControlService(version_control_pb2_grpc.VersionControlServiceServicer):
    sampleData = {
        "addNumbers": [
            {"version": "1.0", "code": "def addNumbers(a, b):\n    return a + b"},
            {"version": "2.0", "code": "def addNumbers(a, b):\n    return a - b"}
        ],
        "findVersions": [
            {"version": "1.0", "code": "for v in self.sampleData[function]:\nif v[\"version\"] != v1:\nv1Code = v[\"code\"]\n"
                                       "if v[\"version\"] == v2:\nv2Code = v[\"code\"]"},
            {"version": "2.0", "code": "for v in self.sampleData[function]:\nif v[\"version\"] == v1:\ncodeV1 = v[\"code\"]\n"
                                       "if v[\"version\"] == v2:\ncodeV2 = v[\"code\"]"},
            {"version": "3.0", "code": "for v in self.sampleData[function]:\nif v[\"version\"] == v1:\nv1Code = v[\"code\"]\n"
                                       "if v[\"version\"] == v2:\nv2Code = v[\"code\"]"}
        ]
    }
    def RollbackToPreviousVersion(self, request, context):
        function = request.function_name
        if function in self.sampleData and len(self.sampleData[function]) > 1:
            self.sampleData[function].pop()
            return version_control_pb2.RollbackResponse(success=True)
        return version_control_pb2.RollbackResponse(success=False)

    def CompareFunctionVersions(self, request, context):
        function, v1, v2 = request.function_name, request.version1, request.version2

        v1Code, v2Code = "", ""
        for v in self.sampleData[function]:
            if v["version"] == v1:
                v1Code = v["code"]
            if v["version"] == v2:
                v2Code = v["code"]
        
        if v1Code == "" or v2Code == "":
            return version_control_pb2.CompareResponse()
        
        v1Code_lines = v1Code.splitlines()
        v2Code_lines = v2Code.splitlines()
        changes = []
        for lineNum, (v1Line, v2Line) in enumerate(zip(v1Code_lines, v2Code_lines)):
            if v1Line != v2Line:
                changes.append(version_control_pb2.Change(line=lineNum + 1, old=v1Line, new=v2Line))
        return version_control_pb2.CompareResponse(changes=changes)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    version_control_pb2_grpc.add_VersionControlServiceServicer_to_server(VersionControlService(), server)


    # Enable reflection for grpcui
    SERVICE_NAMES = (
        version_control_pb2.DESCRIPTOR.services_by_name['VersionControlService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
