import serial
import pynmea2
import time 
import sys

#this code is for logging NMEA 0183 sentences using a raspberry pi from one USB port.

ports = ['/dev/ttyUSB3','/dev/ttyUSB2','/dev/ttyUSB1','/dev/ttyUSB0']

valid = False;
while valid == False:
    
    print('Select a port? (Y/N)')
    x = input()
    if x == 'Y':
        print('Select a port: (0-3)')
        openPort = '/dev/ttyUSB' + input()
        valid = True
    elif x == 'N':
        print ('Scanning ports...')
        valid = True
        for port in ports:
            try:
                ser = serial.Serial(port, 4800, timeout = 1)
                if ser.isOpen() == True:
                    print('Port:' + port + ' is open!')
                    openPort = port
                    break
            except: pass
    else:
        print('Invalid Input')



try:
    ser = serial.Serial(openPort, 4800,timeout = 1)
except:
    print('Device not connected to port' + openPort)
    sys.exit()

if ser.isOpen() == True:
    
    print('Device connected!')
    
    print('Name of log file:')
    fileName = input()
    
    print('How many NMEA sentences do you want to record?')
    num = input()
    
    with open(fileName, 'w') as file:
        with open('parsed' + fileName, 'w') as parsedFile:
            print('Logging Data...')
        
            
            for i in range(int(num)):
                line = ser.readline().decode('ascii', errors='replace')
                file.write(line.strip()+'\n')
                parsedNMEA = pynmea2.parse(line.strip()+'\n')
                parsedFile.write(str(['%s: %s' % (parsedNMEA.fields[i][0], parsedNMEA.data[i]) 
                for i in range(len(parsedNMEA.fields))])+'\n')
                print(line.strip())
                    
            time.sleep(3)
    
    print('Logging complete')
    file.close()
    sys.exit()

else:
    print('Device not connected to port' + openPort)
    sys.exit()
     

#nmea = '$GPRMC,164125,A,4425.8988,N,07543.5370,W,000.0,000.0,151116,,,A*66'
#nmeaobj = pynmea2.parse(nmea)
#print(['%s: %s' % (nmeaobj.fields[i][0], nmeaobj.data[i]) 
     #for i in range(len(nmeaobj.fields))])

