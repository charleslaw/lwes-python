from socket import inet_aton

from lwes.event_marshall import marshall_SHORT_STRING, marshall_LONG_STRING, \
    marshall_BYTE, marshall_BOOLEAN, marshall_U_INT_16, marshall_INT_16, \
    marshall_U_INT_32, marshall_INT_32, marshall_U_INT_64, marshall_INT_64, \
    marshall_IP_ADDR


TYPE_BYTE_VALUE = {
                   'LWES_UNDEFINED_TOKEN': chr(0xff),
                   'LWES_U_INT_16_TOKEN' : chr(0x01),
                   'LWES_INT_16_TOKEN'   : chr(0x02),
                   'LWES_U_INT_32_TOKEN' : chr(0x03),
                   'LWES_INT_32_TOKEN'   : chr(0x04),
                   'LWES_STRING_TOKEN'   : chr(0x05),
                   'LWES_IP_ADDR_TOKEN'  : chr(0x06),
                   'LWES_INT_64_TOKEN'   : chr(0x07),
                   'LWES_U_INT_64_TOKEN' : chr(0x08),
                   'LWES_BOOLEAN_TOKEN'  : chr(0x09),
                   }

TYPE_MARSHALL = {
                 'LWES_U_INT_16_TOKEN' : marshall_U_INT_16,
                 'LWES_INT_16_TOKEN'   : marshall_INT_16,
                 'LWES_U_INT_32_TOKEN' : marshall_U_INT_32,
                 'LWES_INT_32_TOKEN'   : marshall_INT_32,
                 'LWES_STRING_TOKEN'   : marshall_LONG_STRING,
                 'LWES_IP_ADDR_TOKEN'  : marshall_IP_ADDR,
                 'LWES_INT_64_TOKEN'   : marshall_INT_64,
                 'LWES_U_INT_64_TOKEN' : marshall_U_INT_64,
                 'LWES_BOOLEAN_TOKEN'  : marshall_BOOLEAN,
                  }


class LwesEvent(object):
    def __init__(self, db, name, encoding=None):
        if name is None:
            raise Exception('Name required')

        self.event_name = name
        #TODO: Support DB
        self.type_db = db
        self.attributes = {}
        if encoding is None:
            self.encoding_dict = {}
        else:
            self.encoding_dict = encoding


    def __put_attribute(self, name, value, type):
        #TODO: check against the event db (attribute & type)
        self.attributes[name] = {'type': type,
                                 'value': value}

    def set_STRING(self, name, value):
        self.__put_attribute(name, value, 'LWES_STRING_TOKEN')

    def set_U_INT_16(self, name, value):
        self.__put_attribute(name, int(value), 'LWES_U_INT_16_TOKEN')

    def set_INT_16(self, name, value):
        self.__put_attribute(name, int(value), 'LWES_INT_16_TOKEN')

    def set_U_INT_32(self, name, value):
        self.__put_attribute(name, int(value), 'LWES_U_INT_32_TOKEN')

    def set_INT_32(self, name, value):
        self.__put_attribute(name, int(value), 'LWES_INT_32_TOKEN')

    def set_U_INT_64(self, name, value):
        self.__put_attribute(name, long(value), 'LWES_U_INT_64_TOKEN')

    def set_INT_64(self, name, value):
        self.__put_attribute(name, long(value), 'LWES_INT_64_TOKEN')

    def set_BOOLEAN(self, name, value):
        self.__put_attribute(name, bool(value), 'LWES_BOOLEAN_TOKEN')

    def set_IP_ADDR(self, name, value):
        #convert the address to chars
        ip_binary = inet_aton(value)
        self.__put_attribute(name, ip_binary, 'LWES_IP_ADDR_TOKEN')

    def get_bytes(self, output_bytes, num_bytes, offset):
        ret = 0
        if (num_bytes == 0 or offset >= num_bytes):
            return -1

        #start with the event name
        offset, output_bytes \
            = marshall_SHORT_STRING(self.event_name, output_bytes,
                                    num_bytes, offset)

        #then the number of attributes
        offset, output_bytes \
            = marshall_U_INT_16(len(self.attributes), output_bytes,
                                num_bytes, offset)

        #handle encoding first if it is set
        if self.encoding_dict:
            encodingAttr = self.encoding_dict
            encodingValue = encodingAttr['value']
            encodingType = encodingAttr['type']

            if (encodingValue):
                offset, output_bytes = \
                    TYPE_MARSHALL[encodingType](encodingValue, output_bytes,
                                                num_bytes, offset)

        #now iterate over all the values in the hash
        for event_name, event_dict in self.attributes.iteritems():
            tmp_type = event_dict['type']
            type_byte = TYPE_BYTE_VALUE[tmp_type]

            if tmp_type in TYPE_MARSHALL:
                #write the event name
                offset, output_bytes \
                    = marshall_SHORT_STRING(event_name, output_bytes,
                                            num_bytes, offset)
                #write the event type
                offset, output_bytes \
                    = marshall_BYTE (type_byte, output_bytes, num_bytes, offset)

                #write the event value (based on type)
                offset, output_bytes = \
                    TYPE_MARSHALL[tmp_type](event_dict['value'], output_bytes,
                                            num_bytes, offset)
            else:
                raise Exception('Unrecognized attribute type')

        return offset, output_bytes
