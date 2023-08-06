import base64
import io
import json
import logging
import math
import time

import zstd


logger = logging.getLogger(__name__)


class ZstdChunkedHandler(logging.Handler):
    """
    Handler that compresses all input data with ZSTD and flushes it to stdout
    in chunks less than specified size. Each chunk forms a json with metadata
    and valid base64-encoded ZSTD frame. It also flushes data if not enough
    logs (to reach size limit) were written during specified time interval.
    Chunks are delimited with newline.

    This class is not intended to use with small size limits (orders
    of size of compressed log message).
    Size control is heuristic so this class DOES NOT guarantee that resulting
    chunk will not exceed size limit. At least it shouldnt exceed it very much.
    Take care.

    :param stream: Stream to which output will be written.
    :param group_name: Name that will be a part of chunk's metadata.
    :param size_limit: Chunk's size limit in bytes.
    :param flush_every: How many time, in seconds, should the stream wait
    before flush, if not enough data were fed to reach size limit. Zero or
    negative values disable this behavior.
    :param compression_params: Params dict to be passed to ZstdCompressor.
    """

    terminator = '\n'

    def __init__(
        self, stream, group_name, flush_every, size_limit,
        compression_params=None
    ):
        super().__init__()
        self.stream = stream
        self.group_name = group_name
        self.flush_every = flush_every if flush_every > 0 else math.inf
        self.size_limit = size_limit
        self.last_flush = time.monotonic()
        self.compression_params = compression_params or {}

        # considering base64 (hence multiplying by 0.75)
        # 14 is zstd frame header maximum size
        # 200 is reserved for metadata/json overhead
        self._raw_size_limit = int(size_limit * 3 / 4) - 14 - 200

        self._zstd_ctx = zstd.ZstdCompressor(**self.compression_params)
        self._buffer = io.BytesIO()
        self._zstd_stream = self._zstd_ctx.stream_writer(self._buffer)

        # number of bytes zstd stream is buffering at the moment
        self._zstd_buffer_size = 0
        self._raw_bytes_fed = 0

        self._chunk_first_message_ts = None

    @property
    def avg_compression_ratio(self):
        try:
            return self._raw_bytes_fed / self._zstd_stream.tell()
        except ZeroDivisionError:
            pass

    def flush(self):
        self.acquire()
        try:
            self._flush()
        finally:
            self.release()

    def emit(self, record: logging.LogRecord):
        if (
            record.name.startswith('letov') and
            record.msg.startswith('Failed to log record:')
        ):
            # avoid infinite loop, don't log these message with this handler
            return

        if not self._chunk_first_message_ts:
            self._chunk_first_message_ts = record.created

        try:
            self._write(self.format(record) + self.terminator)
        except Exception:
            logger.exception(f'Failed to log record: {record.msg}')

    def close(self):
        self._zstd_stream.close()
        super().close()

    def _format_chunk(self, chunk):
        return json.dumps({
            'data': base64.b64encode(chunk).decode('ascii'),
            'end_ts': time.time(),
            'name': self.group_name,
            'start_ts': self._chunk_first_message_ts,
        })

    def _write_will_overflow(self, data):
        if not self.avg_compression_ratio:
            # first message in a stream
            return False

        estimated_compressed_size = (
            (len(data) + self._zstd_buffer_size) / self.avg_compression_ratio
        )
        return (
            self._raw_size_limit <=
            self._buffer.tell() + estimated_compressed_size
        )

    def _write(self, data):
        data = data.encode('utf-8')

        if self._write_will_overflow(data):
            self._flush()

        self._zstd_buffer_size += len(data)
        compressed_bytes = self._zstd_stream.write(data)
        if compressed_bytes:
            self._raw_bytes_fed += self._zstd_buffer_size
            self._zstd_buffer_size = 0

        if time.monotonic() - self.last_flush >= self.flush_every:
            self._flush()

    def _flush(self):
        if not self._chunk_first_message_ts:
            # its empty
            self.last_flush = time.monotonic()
            return

        self._zstd_stream.flush(zstd.FLUSH_FRAME)

        data = self._format_chunk(self._buffer.getvalue())

        self.stream.write(data + self.terminator)
        self.stream.flush()

        self._buffer.seek(0)
        self._buffer.truncate()

        self._raw_bytes_fed += self._zstd_buffer_size
        self._zstd_buffer_size = 0
        self._chunk_first_message_ts = None

        self.last_flush = time.monotonic()
