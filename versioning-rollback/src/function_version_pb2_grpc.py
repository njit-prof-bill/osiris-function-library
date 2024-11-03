# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import function_version_pb2 as function__version__pb2

GRPC_GENERATED_VERSION = '1.67.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in function_version_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class FunctionVersionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetActiveFunctionVersion = channel.unary_unary(
                '/functionservice.FunctionVersionService/GetActiveFunctionVersion',
                request_serializer=function__version__pb2.GetVersionRequest.SerializeToString,
                response_deserializer=function__version__pb2.GetVersionResponse.FromString,
                _registered_method=True)
        self.SetActiveFunctionVersion = channel.unary_unary(
                '/functionservice.FunctionVersionService/SetActiveFunctionVersion',
                request_serializer=function__version__pb2.SetVersionRequest.SerializeToString,
                response_deserializer=function__version__pb2.SetVersionResponse.FromString,
                _registered_method=True)


class FunctionVersionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetActiveFunctionVersion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetActiveFunctionVersion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FunctionVersionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetActiveFunctionVersion': grpc.unary_unary_rpc_method_handler(
                    servicer.GetActiveFunctionVersion,
                    request_deserializer=function__version__pb2.GetVersionRequest.FromString,
                    response_serializer=function__version__pb2.GetVersionResponse.SerializeToString,
            ),
            'SetActiveFunctionVersion': grpc.unary_unary_rpc_method_handler(
                    servicer.SetActiveFunctionVersion,
                    request_deserializer=function__version__pb2.SetVersionRequest.FromString,
                    response_serializer=function__version__pb2.SetVersionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'functionservice.FunctionVersionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('functionservice.FunctionVersionService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class FunctionVersionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetActiveFunctionVersion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/functionservice.FunctionVersionService/GetActiveFunctionVersion',
            function__version__pb2.GetVersionRequest.SerializeToString,
            function__version__pb2.GetVersionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetActiveFunctionVersion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/functionservice.FunctionVersionService/SetActiveFunctionVersion',
            function__version__pb2.SetVersionRequest.SerializeToString,
            function__version__pb2.SetVersionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
