from enum import Enum


class QueueHeaders(str, Enum):
    NAME = "Name"
    TYPE = "Type"
    STATUS = "Status"


class QueueHeaderTypeValues(str, Enum):
    CREATE = "Create"
    UPDATE = "Update"
