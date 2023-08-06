import json

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from types import MappingProxyType


class LoggingEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, set):
            return tuple(obj)
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, Enum):
            return str(obj)
        elif isinstance(obj, MappingProxyType):
            return dict(obj)
        elif hasattr(obj, 'to_json'):
            return obj.to_json()
        return {'_pyobject': repr(obj)}
