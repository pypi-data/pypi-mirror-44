import json
import logging

from datetime import datetime

from .encoder import LoggingEncoder


logger = logging.getLogger(__name__)


class JsonFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, **kwargs):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.kwargs = kwargs

    def usesTime(self):
        return True

    def format(self, record, etime=None):
        try:
            body = super().format(record)
        except Exception as e:
            logger.error(
                f'Log formatting error: {e}, logrecord_msg: {record.msg}, '
                f'logrecord_args: {record.args}'
            )
            return None

        if etime is None:
            etime = datetime.utcnow()

        info_keys = [
            x for x in record.__dict__ if x not in {'args', 'context'}
        ]
        info = {
            **{key: getattr(record, key, '') for key in info_keys},
            **self.kwargs,
            'created': etime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'loggername': record.name,
            'message': body,
        }
        if record.args and isinstance(record.args, dict):
            info.update(record.args)

        return json.dumps(
            {
                'context': getattr(record, 'context', {}),
                'info': info,
            },
            cls=LoggingEncoder,
        )
