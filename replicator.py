import socket
from discovery import Discovery
import sys
import logging
import serial
import serial.rfc2217 
import time
import threading
import os

class Redirector:
    def __init__(self, serial_instance, socket, debug=None):
        self.serial = serial_instance
        self.socket = socket
        self._write_lock = threading.Lock()
        self.rfc2217 = serial.rfc2217.PortManager(
            self.serial,
            self,
            logger = (debug and logging.getLogger('rfc2217.server'))
            )
        self.log = logging.getLogger('redirector')

    def statusline_poller(self):
        self.log.debug('status line poll thread started')
        while self.alive:
            time.sleep(1)
            self.rfc2217.check_modem_lines()
        self.log.debug('status line poll thread terminated')

    def shortcut(self):
        """connect the serial port to the TCP port by copying everything
           from one side to the other"""
        self.alive = True
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.setDaemon(True)
        self.thread_read.setName('serial->socket')
        self.thread_read.start()
        self.thread_poll = threading.Thread(target=self.statusline_poller)
        self.thread_poll.setDaemon(True)
        self.thread_poll.setName('status line poll')
        self.thread_poll.start()
        self.writer()

    def reader(self):
        """loop forever and copy serial->socket"""
        self.log.debug('reader thread started')
        while self.alive:
            try:
                data = self.serial.read(1)              # read one, blocking
                n = self.serial.inWaiting()             # look if there is more
                if n:
                    data = data + self.serial.read(n)   # and get as much as possible
                if data:
                    # escape outgoing data when needed (Telnet IAC (0xff) character)
                    data = serial.to_bytes(self.rfc2217.escape(data))
                    self._write_lock.acquire()
                    try:
                        self.socket.sendall(data)       # send it over TCP
                    finally:
                        self._write_lock.release()
            except socket.error, msg:
                self.log.error('%s' % (msg,))
                # probably got disconnected
                break
        self.alive = False
        self.log.debug('reader thread terminated')

    def write(self, data):
        """thread safe socket write with no data escaping. used to send telnet stuff"""
        self._write_lock.acquire()
        try:
            self.socket.sendall(data)
        finally:
            self._write_lock.release()

    def writer(self):
        """loop forever and copy socket->serial"""
        while self.alive:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                self.serial.write(serial.to_bytes(self.rfc2217.filter(data)))
            except socket.error, msg:
                self.log.error('%s' % (msg,))
                # probably got disconnected
                break
        self.stop()

    def stop(self):
        """Stop copying"""
        self.log.debug('stopping')
        if self.alive:
            self.alive = False
            self.thread_read.join()
            self.thread_poll.join()



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
            True
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
        print "got keyboard interupt. Breaking"
	listener.keepAlive = False
        break
    except socket.error, msg:
        logging.error('%s' % (msg,))
listener.keepAlive = False
listener.join()
logging.info('--- exit ---')

logging.info('--- exit ---')