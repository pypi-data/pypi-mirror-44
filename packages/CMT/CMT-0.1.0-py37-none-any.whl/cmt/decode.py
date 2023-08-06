import struct
from pathlib import Path

from cmt import utils
from cmt.cmap.v0.cmap import CMap as CMap_0


def decode(file: Path, debug=False):
    with file.open("rb") as reader:
        data = reader.read()
    idx = 0
    identifier = data[idx:idx + 11].decode("utf-8")
    if debug:
        utils.debug_print(data[idx:idx + 11], "identifier", identifier, 0)
    if identifier != "celaria_map":
        raise ValueError("given data is not a Celaria map")

    idx += 11
    version = struct.unpack_from('B', data, idx)[0]
    if debug:
        utils.debug_print((data[idx],), "format version", version, 11)

    if version == 0:
        return CMap_0(data, debug)
    # elif version == 1:
    else:
        raise ValueError(f"cannot read map format version {version}")
