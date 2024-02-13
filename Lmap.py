import sys
import time
import socket
import pyfiglet #To print the logo
import csv #To read the csv file


#Intro for the program
def Intro():
    print(pyfiglet.figlet_format("Lmap",))
    print("""----------------------------------------------------
Usage: python3 Lmap.py [-option] [target_name_or_IP]
To see manual page, type Lmap.py -h
----------------------------------------------------\n""")


#Look up for the port name based on the port number
def LookUpForPortName(port):
	#Read the csv file
	with open('portlist.csv', mode='r') as file:
		reader = csv.reader(file,delimiter=',')
		for row in reader:
			if row[0] == str(port):
				return row[1]
	return 'Unknown'


#Check if user enter target as an IP or a domain name
def CheckTarget(target):
	#if domain name, convert it to IP
	try:
		if any(char.isalpha() for char in target):
			target = socket.gethostbyname(target)
	except socket.gaierror:
		print('Invalid target name or IP')
		sys.exit(0)

	return target


def NormalScan(target):
	print('Normal Scan scan for target:', target, 'in most 20 common ports')
	
	#Scan the 100 most common ports
	mylist = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
	for port in mylist:
		
		#Create a socket object
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#AF_INET: Address Family, IPv4
		#SOCK_STREAM: TCP protocol
		s.settimeout(1)  # Set timeout to 1 seconds
		
		#Connect to the port
		result = s.connect_ex((target, port))
		if result == 0:
			print('Port', port, LookUpForPortName(port), 'is open')

		#Close the socket
		s.close()


def ScanInPortRange(target, start, end):
	print('Scan for target:', target, 'in port range', start, 'to', end)
	
	for port in range(start, end+1):
		
		#Create a socket object
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#AF_INET: Address Family, IPv4
		#SOCK_STREAM: TCP protocol
		s.settimeout(1)  # Set timeout to 1 seconds
		
		#Connect to the port
		result = s.connect_ex((target, port))
		if result == 0:
			print('Port', port, LookUpForPortName(port), 'is open')

		#Close the socket
		s.close()



if __name__ == '__main__':
	
	Intro()
	start_time = time.time()
	

	#Read the mode from the command line
	options = sys.argv[1]
	
	#Check the options
	if options == '-h' or options == '--help':
		print('''
Lmap by CTA
Usage: python3 Lmap [-Options] [target specification]
TARGET SPECIFICATION:
  Can pass hostnames, IP addresses, networks, etc.
  Ex: scanme.nmap.org, microsoft.com/24, 192.168.0.1; 10.0.0-255.1-254
OPTIONS:
  -h: Print help
  -n: Normal scan, which scans the 20 most common ports
 ''')
	elif options == '-n':
		target = sys.argv[len(sys.argv)-1] #Read the target from the command line
		#the last argument in the command line is the target
		target = CheckTarget(target)
		NormalScan(target)
	
	elif options == '-r':
		target = sys.argv[len(sys.argv)-1]
		target = CheckTarget(target)
		start,end = map(int,sys.argv[2].split('-')) #Read the port range from the command line
		ScanInPortRange(target, start, end)

	
	end_time = time.time()
	print('Scan completed in', round(end_time - start_time,4), 'seconds')
	sys.exit(0)
