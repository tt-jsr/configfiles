#!/usr/bin/python
import datetime
import os
import struct
import time
import uuid
import string

# Setting this environment variable causes an alternate protobuf implementation to be used which is
# faster than the native python implementation.  However, several crashes have occurred when using
# it.
# os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "cpp"
#from tt.messaging.header_pb2 import Header
#from tt.messaging.wire_pb2 import Wire

#from tt.messaging.order.new_order_single_pb2 import NewOrderSingle
#from tt.messaging.order.order_cancel_reject_pb2 import OrderCancelReject
#from tt.messaging.order.execution_report_pb2 import ExecutionReport
#from tt.messaging.bookie.bookie_pb2 import (
    #OrderBookDownloadRequest, OrderBookDownloadResponse, SyncRequest, SyncResponse)
#from tt.messaging.order.order_cancel_request_pb2 import OrderCancelRequest
#from tt.messaging.order.order_cancel_replace_request_pb2 import OrderCancelReplaceRequest
#import tt.messaging.order.enums_pb2 as Enums


def unpack_uuid(u):
    return struct.unpack("<QQ", u.bytes)

def pack_uuid(order_id):
    return uuid.UUID(bytes=struct.pack("<QQ", order_id.hi, order_id.lo))

def pack_uuid_hi_low(hi, low):
    return uuid.UUID(bytes=struct.pack("<QQ", hi, low))

def dt_to_ns(d):
    epoch_time = time.mktime(d.timetuple())
    return int(epoch_time * 1000) * 1000000

def get_order_id(er):
    return pack_uuid(er.order_id)

def get_order_id_str(order_id):
    return str(pack_uuid(order_id))

def get_hi_low_id_str(hi, low):
    return str(pack_uuid_hi_low(hi, low))

