"""
Marshall data into the socket message
"""
from struct import pack

#TODO: Use a buffer, or something more efficient than copying strings


def set_output(output_bytes, offset, size, input):
    output_bytes = output_bytes[:offset] + input + output_bytes[:offset+size]
    return output_bytes


def generic_marshall(write_bytes, byte_str, num_bytes, offset, size):

    if byte_str is not None and (num_bytes - offset) >= size:
        byte_str = set_output(byte_str, offset, size, write_bytes)
        offset += size
    return offset, byte_str


def marshall_SHORT_STRING(input, byte_str, num_bytes, offset):
    ret = 0

    #null string is an error so return 0
    if input is None:
        return ret, offset, byte_str

    #need to length to insure it's in bounds
    str_length  = len(input)

    size = str_length + 1
    len_str = chr(str_length)
    if not (str_length < 255 and str_length > 0):
        return ret, offset, byte_str
    #write the length of the string & the string itself
    write_bytes = len_str + input

    return generic_marshall(write_bytes, byte_str, num_bytes, offset, size)

def marshall_LONG_STRING(input, byte_str, num_bytes, offset):
    ret = 0

    #null string is an error so return 0
    if input is None:
        return ret

    #need to length to insure it's in bounds
    two_byte_len = 65535
    str_length  = len(input)
    if str_length > two_byte_len:
        str_length = two_byte_len
        input = input[:two_byte_len]

    size = str_length + 2
    len_str = pack('!H', str_length)
    #write the length of the string & the string itself
    write_bytes = len_str + input

    return generic_marshall(write_bytes, byte_str, num_bytes, offset, size)


def generic_marshall_pack(input, byte_str, num_bytes, offset, size, encoding):
    write_bytes = pack(encoding, input)
    return generic_marshall(write_bytes, byte_str, num_bytes, offset, size)

def marshall_BYTE(input, buffer, num_bytes, offset):
    return generic_marshall_pack(input, buffer, num_bytes, offset, 1, '!c')

def marshall_BOOLEAN(input, buffer, num_bytes, offset):
    return generic_marshall_pack(input, buffer, num_bytes, offset, 1, '!?')

def marshall_U_INT_16(input, buffer, num_bytes, offset):
    return generic_marshall_pack(input, buffer, num_bytes, offset, 2, '!H')

def marshall_INT_16(input, buffer, num_bytes, offset):
    return generic_marshall_pack(input, buffer, num_bytes, offset, 2, '!h')

def marshall_U_INT_32(input, buffer, num_bytes, offset):
    return generic_marshall_pack(input, buffer, num_bytes, offset, 4, '!I')

def marshall_INT_32(input, buffer, num_bytes, offset):
    return generic_marshall_pack(input, buffer, num_bytes, offset, 4, '!i')

def marshall_U_INT_64(input, buffer, num_bytes, offset):
    return generic_marshall_pack(input, buffer, num_bytes, offset, 8, '!Q')

def marshall_INT_64(input, buffer, num_bytes, offset):
    return generic_marshall_pack(input, buffer, num_bytes, offset, 8, '!q')

def marshall_IP_ADDR(input, buffer, num_bytes, offset):
    #For ip addresses, the bytes are sent in reverse order
    input = input[::-1]
    return generic_marshall(input, buffer, num_bytes, offset, 4)
