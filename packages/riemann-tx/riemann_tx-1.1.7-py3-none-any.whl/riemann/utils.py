import hashlib
import riemann
from riemann import blake256 as b256


def i2le(number):
    '''Convert int to little endian (l.e.) bytearray
    Args:
        number  (int): int value to convert to bytes in l.e. format
    Returns:
                (bytearray): bytearray in l.e. format
    '''
    if number == 0:
        return b'\x00'
    return number.to_bytes((number.bit_length() + 7) // 8, 'little')


def i2le_padded(number, length):
    '''Convert int to little endian (l.e.) bytearray with specified length
    Args:
        number  (int): int value to convert to l.e. bytes
        length  (int): length of resulting bytearray
    Returns:
        (bytes)
    '''
    return number.to_bytes(length, 'little')


def i2le_script(number):
    '''Convert int to signed little endian (l.e.) hex for scripts
    Args:
        number  (int): int value to convert to bytes in l.e. format
    Returns:
                (str): the hex-encoded signed LE number
    '''
    if number == 0:
        return '00'
    for i in range(80):
        try:
            return number.to_bytes(
                length=i,  # minimal bytes lol
                byteorder='little',
                signed=True).hex()
        except Exception:
            continue


def le2i(b, signed=False):
    '''Convert little endian (l.e.) bytearray to int
    Args:
        b       (bytearray): l.e. bytearray to convert to int
        signed  (bool): two's complement flag
    Returns:
                (int)
    '''
    return int.from_bytes(b, 'little', signed=signed)


def be2i(b, signed=False):
    '''Convert big endian (b.e.) bytearray to int
    Args:
        b       (bytearray): b.e. bytearray to convert to int
        signed  (bool): two's complement flag
    Returns:
                (int)
    '''
    return int.from_bytes(b, 'big', signed=signed)


def i2be(number):
    '''Convert int to big endian (b.e.) bytearray
    Args:
        number  (int): int value to convert to bytes in b.e. format
    Returns:
                (bytearray): bytearray in b.e. format
    '''
    if number == 0:
        return b'\x00'
    return number.to_bytes((number.bit_length() + 7) // 8, 'big')


def i2be_padded(number, length):
    '''Convert int to big endian (b.e.) bytearray with specified length
    Args:
        number  (int): int value to convert to bytes in b.e. format
        length  (int): length of resulting bytearray
    Returns:
                (bytearray): bytearray in b.e. format with specified length
    '''
    return number.to_bytes(length, 'big')


def change_endianness(b):
    '''
    iter -> iter
    '''
    return b[::-1]


def rmd160(msg_bytes):
    '''
    byte-like -> bytes
    '''
    h = hashlib.new('ripemd160')
    h.update(msg_bytes)
    return h.digest()


def sha256(msg_bytes):
    '''
    byte-like -> bytes
    '''
    return hashlib.sha256(msg_bytes).digest()


def hash160(msg_bytes):
    '''
    byte-like -> bytes
    '''
    h = hashlib.new('ripemd160')
    if 'decred' in riemann.get_current_network_name():
        h.update(blake256(msg_bytes))
        return h.digest()
    h.update(sha256(msg_bytes))
    return h.digest()


def hash256(msg_bytes):
    '''
    byte-like -> bytes
    '''
    if 'decred' in riemann.get_current_network_name():
        return blake256(blake256(msg_bytes))
    return hashlib.sha256(hashlib.sha256(msg_bytes).digest()).digest()


def blake256(msg_bytes):
    '''
    byte-like -> bytes
    '''
    return b256.blake_hash(msg_bytes)


def blake2b(data=b'', **kwargs):
    '''
    byte-like -> bytes
    '''
    b2 = hashlib.blake2b(**kwargs)
    b2.update(data)
    return b2.digest()


def blake2s(data=b'', **kwargs):
    b2 = hashlib.blake2s(**kwargs)
    b2.update(data)
    return b2.digest()
