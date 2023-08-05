import importlib
import logging
import re
import subprocess
from shutil import which

import requests
import msgpack
from tqdm import tqdm

from reprobench.core.exceptions import ExecutableNotFoundError

log = logging.getLogger(__name__)


def find_executable(executable):
    path = which(executable)
    if path is None:
        raise ExecutableNotFoundError
    return path


def silent_run(command):
    log.debug(f"Running: {command}")
    return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def import_class(path):
    module_path, tail = ".".join(path.split(".")[:-1]), path.split(".")[-1]
    module = importlib.import_module(module_path)
    return getattr(module, tail)


def copyfileobj(fsrc, fdst, callback, length=16 * 1024):
    while True:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
        callback(len(buf))


def download_file(url, dest):
    r = requests.get(url, stream=True)

    with tqdm(
        total=int(r.headers["content-length"]),
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        progress_bar.set_postfix(file=dest, refresh=False)
        with open(dest, "wb") as f:
            copyfileobj(r.raw, f, progress_bar.update)


ranged_numbers_re = re.compile(r"(?P<start>\d+)\.\.(?P<end>\d+)(\.\.(?P<step>\d+))?")


def is_range_str(range_str):
    return ranged_numbers_re.match(range_str)


def str_to_range(range_str):
    matches = ranged_numbers_re.match(range_str).groupdict()
    start = int(matches["start"])
    end = int(matches["end"])

    if matches["step"]:
        return range(start, end, int(matches["step"]))
    return range(start, end)


def encode_message(obj):
    return msgpack.packb(obj, use_bin_type=True)


def decode_message(msg):
    return msgpack.unpackb(msg, raw=False)


def send_event(socket, event_type, payload):
    """
    Used in the worker with a DEALER socket
    """
    socket.send_multipart([event_type, encode_message(payload)])


def recv_event(socket):
    """
    Used in the SUB handler
    """
    event_type, payload, address = socket.recv_multipart()

    return event_type, decode_message(payload), address
