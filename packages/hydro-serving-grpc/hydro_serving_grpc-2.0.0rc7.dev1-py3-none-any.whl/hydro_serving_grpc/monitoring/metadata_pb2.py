# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hydro_serving_grpc/monitoring/metadata.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hydro_serving_grpc/monitoring/metadata.proto',
  package='hydrosphere.monitoring',
  syntax='proto3',
  serialized_pb=_b('\n,hydro_serving_grpc/monitoring/metadata.proto\x12\x16hydrosphere.monitoring\x1a\x1bgoogle/protobuf/empty.proto\"\'\n\x0e\x45xecutionError\x12\x15\n\rerror_message\x18\x01 \x01(\t\"$\n\tTraceData\x12\n\n\x02ts\x18\x01 \x01(\x03\x12\x0b\n\x03uid\x18\x02 \x01(\x03\"\x92\x02\n\x11\x45xecutionMetadata\x12\x16\n\x0e\x61pplication_id\x18\x01 \x01(\x03\x12\x10\n\x08stage_id\x18\x02 \x01(\t\x12\x17\n\x0fmodelVersion_id\x18\x03 \x01(\x03\x12\x16\n\x0esignature_name\x18\x04 \x01(\t\x12\x12\n\nrequest_id\x18\x05 \x01(\t\x12\x1e\n\x16\x61pplication_request_id\x18\x06 \x01(\t\x12\x1d\n\x15\x61pplication_namespace\x18\x07 \x01(\t\x12\x12\n\nmodel_name\x18\x08 \x01(\t\x12\x35\n\ntrace_data\x18\n \x01(\x0b\x32!.hydrosphere.monitoring.TraceDataJ\x04\x08\t\x10\nB#\n!io.hydrosphere.serving.monitoringb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_EXECUTIONERROR = _descriptor.Descriptor(
  name='ExecutionError',
  full_name='hydrosphere.monitoring.ExecutionError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error_message', full_name='hydrosphere.monitoring.ExecutionError.error_message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=101,
  serialized_end=140,
)


_TRACEDATA = _descriptor.Descriptor(
  name='TraceData',
  full_name='hydrosphere.monitoring.TraceData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ts', full_name='hydrosphere.monitoring.TraceData.ts', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uid', full_name='hydrosphere.monitoring.TraceData.uid', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=142,
  serialized_end=178,
)


_EXECUTIONMETADATA = _descriptor.Descriptor(
  name='ExecutionMetadata',
  full_name='hydrosphere.monitoring.ExecutionMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='application_id', full_name='hydrosphere.monitoring.ExecutionMetadata.application_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stage_id', full_name='hydrosphere.monitoring.ExecutionMetadata.stage_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='modelVersion_id', full_name='hydrosphere.monitoring.ExecutionMetadata.modelVersion_id', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='signature_name', full_name='hydrosphere.monitoring.ExecutionMetadata.signature_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='request_id', full_name='hydrosphere.monitoring.ExecutionMetadata.request_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='application_request_id', full_name='hydrosphere.monitoring.ExecutionMetadata.application_request_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='application_namespace', full_name='hydrosphere.monitoring.ExecutionMetadata.application_namespace', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='model_name', full_name='hydrosphere.monitoring.ExecutionMetadata.model_name', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trace_data', full_name='hydrosphere.monitoring.ExecutionMetadata.trace_data', index=8,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=181,
  serialized_end=455,
)

_EXECUTIONMETADATA.fields_by_name['trace_data'].message_type = _TRACEDATA
DESCRIPTOR.message_types_by_name['ExecutionError'] = _EXECUTIONERROR
DESCRIPTOR.message_types_by_name['TraceData'] = _TRACEDATA
DESCRIPTOR.message_types_by_name['ExecutionMetadata'] = _EXECUTIONMETADATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExecutionError = _reflection.GeneratedProtocolMessageType('ExecutionError', (_message.Message,), dict(
  DESCRIPTOR = _EXECUTIONERROR,
  __module__ = 'hydro_serving_grpc.monitoring.metadata_pb2'
  # @@protoc_insertion_point(class_scope:hydrosphere.monitoring.ExecutionError)
  ))
_sym_db.RegisterMessage(ExecutionError)

TraceData = _reflection.GeneratedProtocolMessageType('TraceData', (_message.Message,), dict(
  DESCRIPTOR = _TRACEDATA,
  __module__ = 'hydro_serving_grpc.monitoring.metadata_pb2'
  # @@protoc_insertion_point(class_scope:hydrosphere.monitoring.TraceData)
  ))
_sym_db.RegisterMessage(TraceData)

ExecutionMetadata = _reflection.GeneratedProtocolMessageType('ExecutionMetadata', (_message.Message,), dict(
  DESCRIPTOR = _EXECUTIONMETADATA,
  __module__ = 'hydro_serving_grpc.monitoring.metadata_pb2'
  # @@protoc_insertion_point(class_scope:hydrosphere.monitoring.ExecutionMetadata)
  ))
_sym_db.RegisterMessage(ExecutionMetadata)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n!io.hydrosphere.serving.monitoring'))
# @@protoc_insertion_point(module_scope)
