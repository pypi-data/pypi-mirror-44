def bytes_to_int(bts):
    return int.from_bytes(bts, 'big')


def int_to_bytes(i):
    length = max(1, (i.bit_length() + 7) // 8)
    return i.to_bytes(length, 'big')


def hex_to_int(h):
    return int(h, 16)


def str_to_bytes(s):
    return str.encode(s, 'utf-8')


def str_to_int(s):
    return bytes_to_int(str_to_bytes(s))


def int_to_str(i):
    return bytes_to_str(int_to_bytes(i))


def bytes_to_str(b):
    return b.decode('utf-8')


def int_to_hex(i):
    return format(i, 'x')


def bytes_to_hex(b):
    return b.hex()


def hex_to_bytes(h):
    return bytes.fromhex(h)


def str_to_hex(s):
    return bytes_to_hex(str_to_bytes(s))


def hex_to_str(h):
    return bytes_to_str(hex_to_bytes(h))
