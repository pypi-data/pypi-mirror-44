# Wirepas Oy

from ..error_pb2 import *
import enum


class GatewayResultCode(enum.Enum):
    '''
    Class that represent all possible errors generated by a gateway
    Keep a one-to-one mapping with current protobuf errors to ease
    conversion
    '''
    GW_RES_OK = OK
    GW_RES_INTERNAL_ERROR = INTERNAL_ERROR
    GW_RES_INVALID_SINK_ID = INVALID_SINK_ID
    GW_RES_INVALID_ROLE = INVALID_ROLE
    GW_RES_INVALID_NETWORK_ADDRESS = INVALID_NETWORK_ADDRESS
    GW_RES_INVALID_NETWORK_CHANNEL = INVALID_NETWORK_CHANNEL
    GW_RES_INVALID_CHANNEL_MAP = INVALID_CHANNEL_MAP
    GW_RES_INVALID_NETWORK_KEYS = INVALID_NETWORK_KEYS
    GW_RES_INVALID_AC_RANGE = INVALID_AC_RANGE
    GW_RES_INVALID_SINK_STATE = INVALID_SINK_STATE
    GW_RES_INVALID_DEST_ADDRESS = INVALID_DEST_ADDRESS
    GW_RES_INVALID_DEST_ENDPOINT = INVALID_DEST_ENDPOINT
    GW_RES_INVALID_SRC_ENDPOINT = INVALID_SRC_ENDPOINT
    GW_RES_INVALID_QOS = INVALID_QOS
    GW_RES_INVALID_DATA_PAYLOAD = INVALID_DATA_PAYLOAD
    GW_RES_INVALID_SCRATCHPAD = INVALID_SCRATCHPAD
    GW_RES_INVALID_SCRATCHPAD_SIZE = INVALID_SCRATCHPAD_SIZE
    GW_RES_INVLAID_SEQUENCE_NUMBER = INVLAID_SEQUENCE_NUMBER
    GW_RES_INVALID_REBOOT_DELAY = INVALID_REBOOT_DELAY
    GW_RES_INVALID_DIAG_INTERVAL = INVALID_DIAG_INTERVAL
    GW_RES_INVALID_APP_CONFIG = INVALID_APP_CONFIG
    GW_RES_INVALID_PARAM = INVALID_PARAM
    GW_RES_NO_SCRATCHPAD_PRESENT = NO_SCRATCHPAD_PRESENT
    GW_RES_ACCESS_DENIED = ACCESS_DENIED
    GW_RES_REQUEST_NEEDS_SINK_ID = REQUEST_NEEDS_SINK_ID
    GW_RES_INVALID_MAX_HOP_COUNT = INVALID_MAX_HOP_COUNT
