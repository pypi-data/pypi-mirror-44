from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
)

import struct
from io import BytesIO
import os
import decimal
from uuid import UUID, uuid4
from datetime import datetime
import time
from binascii import hexlify, unhexlify

MAGIC=b'Domain'

MAC_BYTES =  b'\x06\x00'
PC_BYTES  =  b'\x00\x06'

MODE_PC  = 1
MODE_MAC = 0

class AVBObjectRef(object):
    __slots__ = ('root', 'index')
    def __init__(self, root, index):
        self.root = root
        self.index = index

    @property
    def value(self):
        if self.index <= 0:
            return None
        if self.root.debug_copy_refs:
            return self

        return self.root.read_object(self.index)

    @property
    def class_id(self):
        if not self.root.check_refs:
            return b'NULL'
        if self.valid:
            chunk = self.root.read_chunk(self.index)
            return chunk.class_id

    @property
    def valid(self):
        if self.index >= len(self.root.object_positions):
            return False
        return True

    def __repr__(self):
        s = "%s.%s"  % (self.__class__.__module__,
                                self.__class__.__name__)
        if self.index and self.valid:
            chunk = self.root.read_chunk(self.index)
            s += " %s idx: %d pos: %d" % (chunk.class_id, self.index, chunk.pos)
        return '<%s at 0x%x>' % (s, id(self))

def reverse_str(s):

    size = len(s)
    result = bytearray(size)
    for i in range(size):
        result[size - 1 - i] = s[i]

    return bytes(result)

def read_s32le(f):
    return struct.unpack(b"<i", f.read(4))[0]

def write_s32le(f, value):
    f.write(struct.pack(b"<i", value))

def read_u32le(f):
    return struct.unpack(b"<I", f.read(4))[0]

def write_u32le(f, value):
    f.write(struct.pack(b"<I", value))

def read_u32be(f):
    return struct.unpack(b">I", f.read(4))[0]

def write_u32be(f, value):
    f.write(struct.pack(b">I", value))

def read_s16le(f):
    return struct.unpack(b"<h", f.read(2))[0]

def write_s16le(f, value):
    f.write(struct.pack(b"<h", value))

def read_u16le(f):
    return struct.unpack(b"<H", f.read(2))[0]

def write_u16le(f, value):
    f.write(struct.pack(b"<H", value))

def read_u8(f):
    return struct.unpack(b"<B", f.read(1))[0]

def write_u8(f, value):
    f.write(struct.pack(b"<B", value))

def read_s8(f):
    return struct.unpack(b"<b", f.read(1))[0]

def write_s8(f, value):
    f.write(struct.pack(b"<b", value))

def read_s64le(f):
    return struct.unpack(b"<q", f.read(8))[0]

def write_s64le(f, value):
    f.write(struct.pack(b"<q", value))

def read_u64le(f):
    return struct.unpack(b"<Q", f.read(8))[0]

def write_u64le(f, value):
    f.write(struct.pack(b"<Q", value))

def read_doublele(f):
    return struct.unpack(b"<d", f.read(8))[0]

def write_doublele(f, value):
    f.write(struct.pack(b"<d", value))

def read_bool(f):
    return read_u8(f) == 0x01

def write_bool(f, value):
    if value:
        write_u8(f, 0x01)
    else:
        write_u8(f, 0x00)

def read_fourcc(f):
    return reverse_str(f.read(4))

def write_fourcc(f, value):
    assert len(value) == 4
    f.write(reverse_str(value))

def read_string(f, encoding = 'macroman'):
    size = read_u16le(f)
    if size >= 65535:
        return u""

    s = f.read(size)
    s = s.strip(b'\x00')
    return s.decode(encoding)

def write_string(f, s, encoding = 'macroman'):
    s = s or b""
    if s == b"":
        write_u16le(f, 0)
        return

    data = s.encode(encoding)

    if encoding == 'utf-8':
        data = b'\x00\x00' + data

    size = len(data)
    write_u16le(f, size)
    f.write(data)

def read_datetime(f):
    return datetime.fromtimestamp(read_u32le(f))

def datetime_to_timestamp(d):
    return int(time.mktime(d.timetuple()))

def write_datetime(f, value):
    write_u32le(f, datetime_to_timestamp(value))

def read_raw_uuid(f):
    return UUID(bytes_le=f.read(16))

def write_raw_uuid(f, value):
    f.write(value.bytes_le)

def read_assert_tag(f, version):
    version_mark = read_u8(f)
    if version_mark != version:
        raise AssertionError("%d != %d" % (version_mark, version))

def read_uuid(f):

    data = b''
    read_assert_tag(f, 72)
    data += f.read(4)

    read_assert_tag(f, 70)
    data += f.read(2)

    read_assert_tag(f, 70)
    data += f.read(2)

    read_assert_tag(f, 65)
    data4len = read_s32le(f)
    assert data4len == 8
    data += f.read(8)

    return UUID(bytes_le=data)

def write_uuid(f, value):

    write_u8(f, 72)
    write_u32le(f, value.time_low)
    write_u8(f, 70)
    write_u16le(f, value.time_mid)
    write_u8(f, 70)
    write_u16le(f, value.time_hi_version)

    write_u8(f, 65)
    write_s32le(f, 8)
    f.write(value.bytes_le[8:])


def int_from_bytes(data, byte_order='big'):
    num = 0
    if byte_order == 'little':
        for i, byte in enumerate(data):
            num += byte << (i * 8)
        return num
    elif byte_order == 'big':
        length = len(data) - 1
        for i, byte in enumerate(data):
            num += byte << ((length-i) * 8)
        return num
    else:
        raise ValueError('endianess must be "little" or "big"')

def bytes_from_int(num, length, byte_order='big'):
    if byte_order == 'little':
        v = bytearray((num >> (i * 8) & 0xff for i in range(length)))
        return bytes(v)
    elif byte_order == 'big':
        v = bytearray((num >> (length - 1 - i) * 8) & 0xff for i in range(length))
        return bytes(v)
    else:
        raise ValueError('endianess must be "little" or "big"')

def read_object_ref(root, f):
    index = read_u32le(f)
    ref =  AVBObjectRef(root, index)
    if not root.check_refs or ref.valid:
        return ref
    raise ValueError("bad index: %d" % index)

def write_object_ref(root, f, value):
    if value is None:
        index = 0
    elif root.debug_copy_refs:
        index = value.index
    elif value.instance_id not in root.ref_mapping:
        raise Exception("object not written yet")
    else:
        index = root.ref_mapping[value.instance_id]

    write_u32le(f, index)

def read_exp10_encoded_float(f):
    mantissa = read_s32le(f)
    exp10 = read_s16le(f)

    return float(mantissa) * pow(10, exp10)

exp10_pretty = {
5994: (59940, -3),
}

def write_exp10_encoded_float(f, value):
    exponent = 0
    while int(value) != value:
        if abs(value * 10) >= 0x7FFFFFFF:
            break
        if exponent <= -6:
            break
        value *= 10
        exponent -= 1

    # remap values pretty values to match seen files
    if value in exp10_pretty:
        write_s32le(f, exp10_pretty[value][0])
        write_s16le(f, exp10_pretty[value][1])
    else:
        write_s32le(f, int(value))
        write_s16le(f, exponent)

def read_rect(f):
    version = read_s16le(f)
    assert version == 1

    a = read_s16le(f)
    b = read_s16le(f)
    c = read_s16le(f)
    d = read_s16le(f)

    return [a,b,c,d]

def write_rect(f, v):
    write_s16le(f, 1)
    write_s16le(f, v[0])
    write_s16le(f, v[1])
    write_s16le(f, v[2])
    write_s16le(f, v[3])

def read_rgb_color(f):
    version = read_s16le(f)
    assert version == 1
    r = read_u16le(f)
    g = read_u16le(f)
    b = read_u16le(f)

    return [r,g,b]

def write_rgb_color(f, v):
    write_s16le(f, 1)
    write_u16le(f, v[0])
    write_u16le(f, v[1])
    write_u16le(f, v[2])

def iter_ext(f):
    while True:
        pos = f.tell()
        tag = read_u8(f)
        if tag != 0x01:
            f.seek(pos)
            break

        tag = read_u8(f)
        yield tag

def peek_data(f, size=None):
    pos = f.tell()
    if size:
        data = f.read(size)
    else:
        data = f.read()
    f.seek(pos)
    return data

def unpack_u16le_from(buffer, offset):
    value  = buffer[offset]
    value += buffer[offset+1] << 8
    return value

def unpack_u32le_from(buffer, offset):
    value  = buffer[offset]
    value += buffer[offset+1] << 8
    value += buffer[offset+2] << 16
    value += buffer[offset+3] << 24
    return value

def generate_uid():
    v = uuid4().int & (1<<64)-1
    return v

AVBClaseID_dict = {}
AVBClassName_dict = {}
def register_class(classobj):
    AVBClaseID_dict[classobj.class_id] = classobj
    AVBClassName_dict[classobj.__name__] = classobj

    return classobj

def register_helper_class(classobj):
    AVBClassName_dict[classobj.__name__] = classobj
    return classobj
