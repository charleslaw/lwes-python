import socket


MAX_MSG_SIZE = 65507


IN_MULTICAST = lambda i: ((ord(i[0]) & 0xf0) == 0xe0)

def lwes_net_open(address, iface, port):

    # set up the address structure
    ip_addr = socket.gethostbyname(address)
    s_addr = socket.inet_aton(ip_addr)
    address = (socket.TIPC_ADDR_NAME, address, port)

    socketfd = socket.socket(socket.AF_INET)

    
    #self.mcast_addr = {'sin_family': AF_INET,
    #                   'sin_addr.s_addr': address, #inet_addr (address
    #                   'sin_port': port #htons ((short)port)
   	#                   }
    
    #socket.inet_aton
    #nl_address = '\x7f\x00\x00\x01'
    '''
      memset((char *) &conn->mcast_addr, 0, sizeof(conn->mcast_addr));
      conn->mcast_addr.sin_family      = ;
      conn->mcast_addr. = );
      conn->mcast_addr.sin_port        = ;
      conn->hasJoined                  = 0;

      /* and the multicast structure (which may not be used if this is a unicast
         connection) */
      conn->mreq.imr_multiaddr = conn->mcast_addr.sin_addr;
      if ( iface == NULL || strcmp("",iface) == 0 )
        {
      conn->mreq.imr_interface.s_addr = htonl (INADDR_ANY);
        }
      else
        {
      conn->mreq.imr_interface.s_addr = inet_addr (iface);
        }
    '''


    #construct the socket
    socketfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  

    #if the address we are emitting on is a multicast address we
    #set the sockopt which uses that interface to emit on, this doesn't
    #work for unicast */
    if IN_MULTICAST(s_addr):
        if iface:
            #TODO: Test that this works
            #TODO: Depending on testing, add a try block around this
            socketfd.setsockopt(socket.IPPROTO_IP,
                                socket.IP_MULTICAST_IF,
                                s_addr)
            #TODO: Investigate setting reuse address (try block around that)
            #  supposedly this is needed for OSx


    # Setting the value for SO_SNDBF , trying for 10*MAX_MSG_SIZE */
    for i in range(10, 0, -1):
        #try to set the buffer size
        buf_size = MAX_MSG_SIZE*i
        try:
            socketfd.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buf_size)
            break
        except:
            pass
    else:
        #got to 0 and did not set the buffer size
        raise Exception('Could not set buffer size')
    

    #Connect to the server
    #TODO: investigate what happens if the connection is closed!!!!
    socketfd.connect((ip_addr , port))


    return socketfd
