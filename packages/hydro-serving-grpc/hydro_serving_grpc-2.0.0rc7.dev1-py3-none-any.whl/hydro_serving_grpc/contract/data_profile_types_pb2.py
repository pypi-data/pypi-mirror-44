# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hydro_serving_grpc/contract/data_profile_types.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='hydro_serving_grpc/contract/data_profile_types.proto',
  package='hydrosphere.contract',
  syntax='proto3',
  serialized_pb=_b('\n4hydro_serving_grpc/contract/data_profile_types.proto\x12\x14hydrosphere.contract*\xa9\x01\n\x0f\x44\x61taProfileType\x12\x08\n\x04NONE\x10\x00\x12\x0f\n\x0b\x43\x41TEGORICAL\x10\x01\x12\x0b\n\x07NOMINAL\x10\x0b\x12\x0b\n\x07ORDINAL\x10\x0c\x12\r\n\tNUMERICAL\x10\x02\x12\x0e\n\nCONTINUOUS\x10\x15\x12\x0c\n\x08INTERVAL\x10\x16\x12\t\n\x05RATIO\x10\x17\x12\t\n\x05IMAGE\x10\x03\x12\t\n\x05VIDEO\x10\x04\x12\t\n\x05\x41UDIO\x10\x05\x12\x08\n\x04TEXT\x10\x06\x42 \n\x1eio.hydrosphere.serving.managerb\x06proto3')
)

_DATAPROFILETYPE = _descriptor.EnumDescriptor(
  name='DataProfileType',
  full_name='hydrosphere.contract.DataProfileType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CATEGORICAL', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NOMINAL', index=2, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ORDINAL', index=3, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NUMERICAL', index=4, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONTINUOUS', index=5, number=21,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INTERVAL', index=6, number=22,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RATIO', index=7, number=23,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IMAGE', index=8, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO', index=9, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AUDIO', index=10, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TEXT', index=11, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=79,
  serialized_end=248,
)
_sym_db.RegisterEnumDescriptor(_DATAPROFILETYPE)

DataProfileType = enum_type_wrapper.EnumTypeWrapper(_DATAPROFILETYPE)
NONE = 0
CATEGORICAL = 1
NOMINAL = 11
ORDINAL = 12
NUMERICAL = 2
CONTINUOUS = 21
INTERVAL = 22
RATIO = 23
IMAGE = 3
VIDEO = 4
AUDIO = 5
TEXT = 6


DESCRIPTOR.enum_types_by_name['DataProfileType'] = _DATAPROFILETYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\036io.hydrosphere.serving.manager'))
# @@protoc_insertion_point(module_scope)
