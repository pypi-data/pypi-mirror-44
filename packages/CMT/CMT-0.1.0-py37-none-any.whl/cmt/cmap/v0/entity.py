import struct
from abc import ABC
from enum import Enum

from cmt import utils


class Entity(ABC):
    """
    :ivar type: entity type
    :ivar byte_size: size in bytes the entity uses
    """

    def __init__(self, type_: int, byte_size: int):
        self.type = type_
        self.byte_size = byte_size

    def encode(self) -> bytearray:
        """
        Includes the entity type.
        :return:
        """
        raise NotImplementedError


class BlockType(Enum):
    Nothing = 0  # white
    Finish = 1  # red
    Jump = 2  # green
    Speed = 3  # yellow
    Ice = 4  # blue
    Checkpoint = 5  # purple


class Block(Entity):
    """

    :param data:
    :param offset: without entity type byte
    :param debug:
    """

    def __init__(self, data: bytes, offset: int, debug=False):
        super().__init__(0, 30)
        self.block_type = BlockType(utils.unpack_from('B', data, offset, ("block type",), debug)[0])
        # +1 additional due to unused byte
        offset += 1
        utils.unpack_from('B', data, offset, ("unused",), debug)
        offset += 1
        self.position = utils.unpack_from('iiI', data, offset, ("position x", "position y", "position z"), debug)
        offset += 3 * 4
        self.scale = utils.unpack_from('III', data, offset, ("scale x", "scale y", "scale z"), debug)
        offset += 3 * 4
        self.rotation_z = utils.unpack_from('f', data, offset, ("rotation z",), debug)[0]
        offset += 4
        self.checkpoint_nr = -1
        if self.block_type == BlockType.Checkpoint:
            self.checkpoint_nr = utils.unpack_from('B', data, offset, ("checkpoint nr",), debug)[0]
            self.byte_size += 1

    def __str__(self):
        return f"type: 0 [Block]\n" \
            f"block type: {self.block_type.value} [{self.block_type.name}]\n" \
            f"position: {self.position}\n" \
            f"scale: {self.scale}\n" \
            f"rotation z: {self.rotation_z}" \
            "" if self.block_type != 5 else f"\ncheckpoint nr: {self.checkpoint_nr}"

    def encode(self) -> bytearray:
        data = bytearray()
        # entity type
        data.extend(struct.pack('B', self.type))
        # block type
        data.extend(struct.pack('B', self.block_type.value))
        # unused byte
        data.extend(b'\x00')
        # position
        data.extend(struct.pack('iiI', *self.position))
        # scale
        data.extend(struct.pack('III', *self.scale))
        # rotation z
        data.extend(struct.pack('f', self.rotation_z))
        if self.block_type == BlockType.Checkpoint:
            data.extend(struct.pack('B', self.checkpoint_nr))
        return data


class Sphere(Entity):
    """

    :param data:
    :param offset: without entity type byte
    :param debug:
    """

    def __init__(self, data: bytes, offset: int, debug=False):
        super().__init__(1, 12)
        self.position = utils.unpack_from('iii', data, offset, ("position x", "position y", "position z"), debug)

    def __str__(self):
        return f"type: 1 [Sphere]\n" \
            f"position: {self.position}"

    def encode(self) -> bytearray:
        data = bytearray()
        # entity type
        data.extend(struct.pack('B', self.type))
        # position
        data.extend(struct.pack('iii', *self.position))
        return data


class PlayerStart(Entity):
    """

    :param data:
    :param offset: without entity type byte
    :param debug:
    """

    def __init__(self, data: bytes, offset: int, debug=False):
        super().__init__(2, 17)
        # one unused byte
        utils.unpack_from('B', data, offset, ("unused",), debug)
        offset += 1
        self.position = utils.unpack_from('iii', data, offset, ("position x", "position y", "position z"), debug)
        offset += 3 * 4
        self.rotation_z = utils.unpack_from('f', data, offset, ("rotation z",), debug)[0]

    def __str__(self):
        return f"type: 2 [PlayerStart]\n" \
            f"position: {self.position}\n" \
            f"rotation z: {self.rotation_z}"

    def encode(self) -> bytearray:
        data = bytearray()
        # entity type
        data.extend(struct.pack('B', self.type))
        # unused byte
        data.extend(b'\x00')
        # position
        data.extend(struct.pack('iii', *self.position))
        # rotation z
        data.extend(struct.pack('f', self.rotation_z))
        return data


class Dummy(Entity):
    """

    :param data:
    :param offset: without entity type byte
    :param debug:
    """

    def __init__(self, data: bytes, offset: int, debug=False):
        super().__init__(128, 29)
        self.id = utils.unpack_from('B', data, offset, ("id",), debug)[0]
        offset += 1
        self.position = utils.unpack_from('iiI', data, offset, ("position x", "position y", "position z"), debug)
        offset += 3 * 4
        self.scale = utils.unpack_from('III', data, offset, ("scale x", "scale y", "scale z"), debug)
        offset += 3 * 4
        self.rotation_z = utils.unpack_from('f', data, offset, ("rotation z",), debug)[0]

    def __str__(self):
        return f"type: 128 [Dummy]\n" \
            f"id: {self.id}\n" \
            f"position: {self.position}\n" \
            f"scale: {self.scale}\n" \
            f"rotation z: {self.rotation_z}"

    def encode(self) -> bytearray:
        data = bytearray()
        # entity type
        data.extend(struct.pack('B', self.type))
        # id
        data.extend(struct.pack('B', self.id))
        # position
        data.extend(struct.pack('iiI', *self.position))
        # scale
        data.extend(struct.pack('III', *self.scale))
        # rotation z
        data.extend(struct.pack('f', self.rotation_z))
        return data
