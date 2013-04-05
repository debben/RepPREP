from xml.etree import ElementTree as ET
import socket
import commands
import threading

HOST = '224.0.0.1'


class Discovery(threading.Thread):
	def getDriver(self):
		threading.Thread.__init__(self)
		machine = ET.ElementTree(file='machine.xml')
		driver = machine.find('driver')
		driver.attrib["port"] = '7000'
		driver.attrib['useRFC2217'] = 'true'


		link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		ifconfig = commands.getoutput("/sbin/ifconfig")
		start = ifconfig.find('inet addr:',ifconfig.find('wlan'),len(ifconfig)) + 11
		end = ifconfig.find(' ',start,len(ifconfig))
		driver.attrib['addr']=ifconfig[start:end]
		return ET.tostring(machine.getroot(), encoding="us-ascii", method="xml")

	def __init__(self, port):
		self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.reply = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.driver = self.getDriver()
		self.port = port

	def run(self):
		print "Listening for pings..."
		self.listener.bind((HOST,self.port))
		while 1:
		    data, addr = self.listener.recvfrom(1024);
		    if not data: continue
		    
		    print "Ping recieved. Replying to ", addr[0]
		    self.reply.connect((addr[0],self.port+1))
		    self.reply.send(self.driver)
		    self.reply.close()


