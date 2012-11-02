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
event.set_U_INT_16('unsigned_int', 42)
event.set_INT_16('signed_int', -1)

emitter.emit(event)
