from abc import ABC, abstractmethod


class ACMap(ABC):
    def __init__(self, version: int):
        self.identifier = "celaria_map"
        self.format_version = version

    @abstractmethod
    def decode(self, data: bytes, debug=False):
        raise NotImplementedError

    @abstractmethod
    def encode(self) -> bytearray:
        raise NotImplementedError
