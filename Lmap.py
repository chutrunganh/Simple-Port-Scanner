#!/usr/bin/python3
import sys
import socket
import pyfiglet      # To print the logo
import csv
import threading     # To create multiple threads

# ANSI escape codes for text colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'  # Reset color to default

# Intro for the program
def print_intro():
    print(RED + pyfiglet.figlet_format("Lmap", font="slant") + RESET)
    print("-" * 50)
    print("Usage: ./Lmap.py [-option] [target_name_or_IP]")
    print("To see manual page, type Lmap.py -h or --help")
    print("-" * 50)
    print("")

# Look up for the port name based on the port number from the csv file
def lookup_port_name(port):
    with open('portlist.csv', mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            if row[0] == str(port):
                return row[1]
    return 'Unknown'

# Check if user entered target as an IP or a domain name
def check_target(target):
    try: 
        # If domain name, convert it to IP
        if any(char.isalpha() for char in target):
            target = socket.gethostbyname(target)
    except socket.gaierror:
        print('Invalid target name or IP')
        sys.exit(0)

    return target

# Check if the port is open
def check_port_is_open(target, port):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #AF_INET: Address Family, IPv4
	#SOCK_STREAM: TCP protocol
    s.settimeout(1) # Set timeout to 1 seconds

    # Connect to the port
    result = s.connect_ex((target, port))
    if result == 0:
        print(GREEN + "[*]" + RESET + 'Port ' + str(port) + ': ' + str(lookup_port_name(port)))
    # else:
    #     print(RED + "[*]" + RESET + 'Port', port, ':', lookup_port_name(port))
    s.close()

# Scan the 20 most common ports
def normal_scan(target):
    print('Normal Scan scan for target:', target, 'in most 20 common ports', '\n')
    mylist = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
    for port in mylist:
        thread = threading.Thread(target=check_port_is_open, args=(target, port))
        thread.start()

# Scan in a port range
def scan_in_port_range(target, start, end):
    print('Scan for target:', target, 'in port range', start, 'to', end, '\n')
    for port in range(start, end + 1):
        thread = threading.Thread(target=check_port_is_open, args=(target, port))
        thread.start()

if __name__ == '__main__':
    print_intro()

    #Read the options from the command line
    options = sys.argv[1] if len(sys.argv) > 1 else None

    #Check the options
    if options in ['-h', '--help']:
        print('''
Lmap by CTA
Usage: ./Lmap [-Options] [target specification]

TARGET SPECIFICATION:
  Specify hostnames, IP addresses, networks, etc.
  Example: scanme.nmap.org, microsoft.com/24, 192.168.0.1; 10.0.0-255.1-254
  NOTE: Port scanning to a target without permission may be considered
    illegal in some countries.
OPTIONS:
  -h: Print help
  -n: Perform a normal scan, checking the 20 most common ports
  -r: Perform a scan within a port range. Specify the range as -r start-end

        ''')
    elif options == '-n':
        #Read the target from the command line
		#the last argument in the command line is the target
        target = sys.argv[-1] if len(sys.argv) > 2 else None
        target = check_target(target)
        normal_scan(target)

    elif options == '-r':
        target = sys.argv[-1] if len(sys.argv) > 2 else None
        target = check_target(target)
        start, end = map(int, sys.argv[2].split('-')) if len(sys.argv) > 3 else (None, None)
        if start is not None and end is not None:
            scan_in_port_range(target, start, end)

    sys.exit(0)