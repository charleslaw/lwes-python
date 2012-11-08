from lwes.lwes_net import lwes_net_open, MAX_MSG_SIZE


class LwesEmitter(object):
    def __init__(self, address, iface, port, heartbeat_flag, heartbeat_freq,
                 ttl=3):

        #try to open a connection
        #try:
        self.connection = lwes_net_open(address, iface, port)
        #    #self.lwes_net_set_ttl(ttl)
        #except:
        #    pass

        #self.buffer =     LWES_BYTE_P
        self.buffer = ' ' * (MAX_MSG_SIZE)
        self.count = 0
        self.count_since_last_beat = 0
        self.sequence = 0
        self.frequency = heartbeat_freq
        self.emitHeartbeat = heartbeat_flag

        # Send an event saying we are starting up if heartbeat is enamed
        if (self.emitHeartbeat):
            pass
            '''
            tmp_event = lwes_event_create(NULL,(LWES_SHORT_STRING)"System::Startup")
              if ( tmp_event != NULL )
            {
              emitter->last_beat_time = time (NULL);
              lwes_emitter_emit_event (emitter,tmp_event);
              lwes_event_destroy (tmp_event);
            }
            '''


    def emit(self, event):
        #/* Send an event */
        error = self.emit_event(event)
        #self.collect_statistics()

    def emit_event(self, event):
        size, self.buffer = event.get_bytes(self.buffer, MAX_MSG_SIZE, 0)
        self.emit_bytes(self.buffer[:size])

    def emit_bytes(self, buffer):
        self.connection.send(buffer)

