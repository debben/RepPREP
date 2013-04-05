import socket
from discovery import Discovery
import sys
import logging
import serial
import serial.rfc2217

#configure the network discovery listener
listener = Discovery(5225)
listener.start()

ADDR = ('',5225)
BUFFSIZE = 4096



'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen(1)
print "Awaiting connection..."
conn, addr = server.accept()
print 'got connection from ', addr[0]
while 1:
  data = conn.recv((1024))
  if data:
      print data
  else:
    conn.close()

'''
level = (
    logging.WARNING,
    logging.INFO,
    logging.DEBUG,
    logging.NOTSET,
    )[3]
logging.basicConfig(level=logging.INFO)
logging.getLogger('root').setLevel(logging.INFO)
logging.getLogger('rfc2217').setLevel(level)


# connect to serial port
ser = serial.Serial()
ser.port     = '/dev/ttyUSB0'
ser.timeout  = 3     # required so that the reader thread can exit

logging.info("RFC 2217 TCP/IP to Serial redirector - type Ctrl-C / BREAK to quit")

try:
    ser.open()
except serial.SerialException, e:
    logging.error("Could not open serial port %s: %s" % (ser.portstr, e))
    sys.exit(1)

logging.info("Serving serial port: %s" % (ser.portstr,))
settings = ser.getSettingsDict()
# reset control line as no _remote_ "terminal" has been connected yet
ser.setDTR(False)
ser.setRTS(False)

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind( ('', 7000) )
srv.listen(1)
logging.info("TCP/IP port: %s" % (7000,))
while True:
    try:
        connection, addr = srv.accept()
        logging.info('Connected by %s:%s' % (addr[0], addr[1]))
        connection.setsockopt( socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        ser.setRTS(True)
        ser.setDTR(True)
        # enter network <-> serial loop
        r = Redirector(
            ser,
            connection,
            options.verbosity > 0
        )
        try:
            r.shortcut()
        finally:
            logging.info('Disconnected')
            r.stop()
            connection.close()
            ser.setDTR(False)
            ser.setRTS(False)
        # Restore port settings (may have been changed by RFC 2217 capable
        # client)
        ser.applySettingsDict(settings)
    except KeyboardInterrupt:
        break
    except socket.error, msg:
        logging.error('%s' % (msg,))

logging.info('--- exit ---')