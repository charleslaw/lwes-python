import struct

MAX_MSG_SIZE = 65507
LWES_ENCODING  = "enc"

from lwes.event_marshall import marshall_SHORT_STRING, marshall_LONG_STRING, \
    marshall_U_INT_16, marshall_BYTE, marshall_INT_16




TYPE2_DICT = {
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
                 #'LWES_U_INT_32_TOKEN' : marshall_U_INT_32,
                 #'LWES_INT_32_TOKEN'   : marshall_INT_32,
                 'LWES_STRING_TOKEN'   : marshall_LONG_STRING,
                 #'LWES_IP_ADDR_TOKEN'  : marshall_IP_ADDR,
                 #'LWES_INT_64_TOKEN'   : marshall_INT_64,
                 #'LWES_U_INT_64_TOKEN' : marshall_U_INT_64,
                 #'LWES_BOOLEAN_TOKEN'  : marshall_BOOLEAN,
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
                if encodingType == LWES_INT_16_TOKEN:
                    ret, offset, output_bytes \
                        = marshall_SHORT_STRING(str(LWES_ENCODING),
                                                output_bytes,
                                                num_bytes,
                                                offset)
                    
                    #TODO: fix this
                    '''
                    if (marshall_SHORT_STRING
                        ((LWES_SHORT_STRING)LWES_ENCODING,
                         output_bytes,
                         num_bytes,
                         &offset) == 0
                      ||
                      marshall_BYTE
                        (encodingType,
                         output_bytes,
                         num_bytes,
                         &offset) == 0
                      ||
                      marshall_INT_16
                        (*((LWES_INT_16 *)encodingValue),
                         output_bytes,
                         num_bytes,
                         &offset) == 0)
                    {
                      return -2;
                    }
                    '''
        
        #now iterate over all the values in the hash
        for event_name, event_dict in self.attributes.iteritems():
            tmp_type = event_dict['type']
            type_byte = TYPE2_DICT[tmp_type]
            
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
