from lwes.emitter import LwesEmitter
from lwes.event import LwesEvent

#Create an emitter to send messages
address = '127.0.0.1'
interface = '' #Not yet supported
port = 20402
heartbeat_flag = 0 #Not yet supported
heartbeat_freq = 0 #Not yet supported

emitter = LwesEmitter(address, interface, port,
                      heartbeat_flag, heartbeat_freq, ttl=1)


db = None
event = LwesEvent (db, 'My LWES Event')


event.set_STRING("Hello", 'World')
event.set_U_INT_16('unsigned_int16', 42)
event.set_INT_16('signed_int16', -1)
event.set_U_INT_32('unsigned_int32', 75535)
event.set_INT_32('signed_int32', -42768)
event.set_U_INT_64('unsigned_int64', 5294967295)
event.set_INT_64('signed_int64', -314748364)
event.set_BOOLEAN('boolT', True)
event.set_BOOLEAN('boolF', False)
event.set_IP_ADDR('addr', '127.1.255.3')

emitter.emit(event)
