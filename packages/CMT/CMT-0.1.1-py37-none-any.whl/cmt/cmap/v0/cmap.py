import struct

from cmt import utils
from cmt.cmap.a_cmap import ACMap
from cmt.cmap.v0.entity import Block, Dummy, PlayerStart, Sphere
from cmt.cmap.v0.medal_times import MedalTimes


class CMap(ACMap):
    """
Celaria .cmap format (version 0) www.celaria.com

Legend (datatype):
===============================
uByte > unsigned byte (1 byte)
uShort > unsigned short (2 bytes)
uInt > unsigned int (4 bytes)
sShort > signed short (2 bytes)
sInt > signed int (4 bytes)
f32 > float (4 bytes)
f64 > double (8 bytes)

---
> [datatype] ( [number of datatypes in sequence] ) - [ [description ] ]

optional:

> [VariableName] : [datatype] ( [number of datatypes in sequence] ) - [ [description ] ]

--
===============================
>>>>>>>>>>>>>>>
>>> cmap format bytesequence
>>>>>>>>>>>>>>>

> uByte (11) - [stringidentifier]
> uByte (1) - [version]

> nameLen: uByte (1) - [number of characters in mapname]
> uByte (nameLen) - [mapname as String]

> timer enabled : uByte (1) - if the timer will be run in singleplayer

> uByte (1) - [unused byte]

> times : uByte (1) - number of checkpoint times (including medal time)

> uInt (times) - [checkpoint times for platin]
> uInt (times) - [checkpoint times for gold]
> uInt (times) - [checkpoint times for silver]
> uInt (times) - [checkpoint times for bronze]

> f32 (1) - [sun rotation on Z axis]
> f32 (1) - [sun height expressed as an angle (between 0 and 90 degrees)]

> f64 (3) - [preview camera position as 3d vektor (x,y and z)]
> f64 (3) - [preview camera lookat position as 3d vektor (x,y and z)]

> entityNR : uInt (1) - [number of entities on the map]

//repeat as often as "entityNR" in a loop:

> entityType: uByte (1) - [entityType]

if(entityType == 0){ //block entity
    > blockType : uByte (1) - [blockType/color]
    > uByte (1) - [unused byte]
    > sInt (2) - [position (x,y)]
    > uInt (1) - [position (z)]
    > uInt (3) - [scale (x,y and z)]
    > f32 (1) - [rotation on Z axis]

    if(blockType == 5){ //checkpoint block
        > uByte (1) - [checkpoint Number]
    }
}

if(entityType == 1){ //sphere entity
     > sInt (3) - [position (x,y and z)]
}

if(entityType == 2){ //playerStart
    > uByte (1) - [type (unused)]
    > sInt (3) - [position (x,y and z)]
    > f32 (1) - [rotation on Z axis]
}


if(entityType == 128){ //dummy entity
    > uByte (1) - [ID]
    > sInt (2) - [position (x,y)]
    > uInt (1) - [position (z)]
    > uInt (3) - [scale (x,y,z)]
    > f32 (1) - [rotation on Z axis]
}

// repeatEnd
    """

    def __init__(self, data: bytes = None, debug=False):
        super().__init__(0)
        self.name = ""
        self.timer_enabled = True
        self.medal_times = None
        self.sun_rotation = 0.0
        self.sun_angle = 0.0
        self.camera_pos = (0.0, 0.0, 0.0)
        self.camera_look = (0.0, 0.0, 0.0)
        self.entities = []

        if data is not None:
            self.decode(data, debug)

    def __str__(self):
        return f"identifier: {self.identifier}\n" \
            f"format version: {self.format_version}\n" \
            f"name: {self.name}\n" \
            f"timer enabled: {self.timer_enabled}\n" \
            f"medal times: {self.medal_times}\n" \
            f"sun rotation: {self.sun_rotation}\n" \
            f"sun angle: {self.sun_angle}\n" \
            f"camera position: {self.camera_pos}\n" \
            f"camera look: {self.camera_look}\n" \
            f"entities: {len(self.entities)}"

    def decode(self, data: bytes, debug=False):
        # name, starts at 12b
        offset = 12

        name_len = utils.unpack_from('B', data, offset, ("name length",), debug)[0]
        offset += 1

        self.name = data[offset:offset + name_len].decode("utf-8")
        if debug:
            utils.debug_print(data[offset:offset + name_len], "name", self.name, offset)
        offset = 13 + name_len

        self.timer_enabled = utils.unpack_from('?', data, offset, ("timer enabled",), debug)
        offset += 1
        utils.unpack_from('B', data, offset, ("unused",), debug)
        offset += 1

        # medal times
        self.medal_times = MedalTimes(data, offset, debug)
        # medal times * 4 (platin, gold, silver, bronze) * 4 bytes
        offset += 1 + len(self.medal_times.platin) * 4 * 4

        self.sun_rotation = utils.unpack_from('f', data, offset, ("sun rotation",), debug)[0]
        offset += 4

        self.sun_angle = utils.unpack_from('f', data, offset, ("sun angle",), debug)[0]
        offset += 4

        self.camera_pos = utils.unpack_from('ddd', data, offset, ("camera pos x", "camera pos y", "camera pos z"),
                                            debug)
        offset += 3 * 8

        self.camera_look = utils.unpack_from('ddd', data, offset, ("camera look x", "camera look y", "camera look z"),
                                             debug)
        offset += 3 * 8

        # entities processing
        ent_count = utils.unpack_from('I', data, offset, ("entity count",), debug)[0]
        offset += 4

        ent_done = 0

        while ent_done < ent_count:
            ent_type = utils.unpack_from('B', data, offset, ("entity type",), debug)[0]
            offset += 1
            if ent_type == 0:
                cur_ent = Block(data, offset, debug)
                self.entities.append(cur_ent)
                offset += cur_ent.byte_size
            elif ent_type == 1:
                cur_ent = Sphere(data, offset, debug)
                self.entities.append(cur_ent)
                offset += cur_ent.byte_size
            elif ent_type == 2:
                cur_ent = PlayerStart(data, offset, debug)
                self.entities.append(cur_ent)
                offset += cur_ent.byte_size
            elif ent_type == 128:
                cur_ent = Dummy(data, offset, debug)
                self.entities.append(cur_ent)
                offset += cur_ent.byte_size
            else:
                raise ValueError(f"Unknown entity type: {ent_type} at {offset - 1}")
            ent_done += 1
        if debug:
            print(offset, " / ", len(data), " consumed")

    def encode(self) -> bytearray:
        data = bytearray()
        # file identifier
        data.extend("celaria_map".encode("utf-8"))
        # format version
        data.extend(struct.pack('B', self.format_version))
        # length of name
        data.extend(struct.pack('B', len(self.name)))
        # name
        data.extend(self.name.encode("utf-8"))
        # timer enabled
        data.extend(struct.pack('?', self.timer_enabled))
        # unused byte
        data.extend(b'\x00')
        # medal times, including the length byte
        data.extend(self.medal_times.encode())
        # sun rotation
        data.extend(struct.pack('f', self.sun_rotation))
        # sun angle
        data.extend(struct.pack('f', self.sun_angle))
        # camera position
        data.extend(struct.pack('ddd', *self.camera_pos))
        # camera look
        data.extend(struct.pack('ddd', *self.camera_look))
        # entity count
        data.extend(struct.pack('I', len(self.entities)))
        # entities
        for ent in self.entities:
            data.extend(ent.encode())
        return data
