import hashlib

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])

# tag::source4[]
def hash160(s):
    '''sha256 followed by ripemd160'''
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()  # <1>
# end::source4[]

def hash256(s):
    '''two rounds of sha256'''
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result
      
# little_endian_to_int() получает байты в порядке Python и инерпертирует их в прямом порядке
# и возвращает целое число
def little_endian_to_int(b):
    '''little_endian_to_int takes byte sequence as a little-endian number.
    Returns an integer'''
    return int.from_bytes(b, 'little')
# int_endian_to_little_endian() выполняет действие противоположное little_endian_to_int()
#
def int_to_little_endian(n, length):
    '''endian_to_little_endian takes an integer and returns the little-endian
    byte sequence of length'''
    return n.to_bytes(length, 'little')

def read_varint(s):
    '''Эта функция читает переменное целое число из потока'''
    i = s.read(1)[0]
    if i == 0xfd:
        # 0xfd означает следующие два байта, обозначающие число
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        # 0xfe означает следующие четыре байта, обозначающие число
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        # 0xff означает следующие восемь байтов, обозначающие число
        return little_endian_to_int(s.read(8))
    else:
        # все остальное является всего лишь целым числом
        return i
    
def encode_varint(i):
    '''Кодируем целое число в виде варианта'''
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise ValueError('integer too large: {}'.format(i))
