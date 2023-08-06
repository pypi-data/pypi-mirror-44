import struct

from cmt import utils


class MedalTimes:
    """
    :param offset: offset contains times count byte.
    """

    def __init__(self, data: bytes, offset: int, debug=False):
        times = utils.unpack_from('B', data, offset, ("medal times",), debug)[0]
        offset += 1
        # we do not use iter_unpack because its easier to use the offset debugging
        self.platin = []
        for i in range(times):
            self.platin.append(utils.unpack_from('I', data, offset, ("platin time",), debug)[0])
            offset += 4

        self.gold = []
        for i in range(times):
            self.gold.append(utils.unpack_from('I', data, offset, ("gold time",), debug)[0])
            offset += 4

        self.silver = []
        for i in range(times):
            self.silver.append(utils.unpack_from('I', data, offset, ("silver time",), debug)[0])
            offset += 4

        self.bronze = []
        for i in range(times):
            self.bronze.append(utils.unpack_from('I', data, offset, ("bronze time",), debug)[0])
            offset += 4

    def __str__(self):
        return f"platin: {self.platin} | gold: {self.gold} | silver: {self.silver} | bronze: {self.bronze}"

    def encode(self) -> bytearray:
        """
        Includes the length byte at the beginning.
        :return:
        """
        data = bytearray()
        # medal times
        data.extend(struct.pack('B', len(self.platin)))
        # medal platin
        for time in self.platin:
            data.extend(struct.pack('I', time))
        # medal gold
        for time in self.gold:
            data.extend(struct.pack('I', time))
        # medal silver
        for time in self.silver:
            data.extend(struct.pack('I', time))
        # medal bronze
        for time in self.bronze:
            data.extend(struct.pack('I', time))
        return data
