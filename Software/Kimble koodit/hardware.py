import serial
import time

def openSerial():
    global s
    s = serial.Serial("COM9",115200) #/dev/cu.usbserial-DN03VXG 
    return 1

def closeSerial():
    s.close()
    

def homing():
    # Open grbl serial port
    siirto = '$H\n'
    string = '$#\n'
    #Wake up grbl
    s.write(string.encode('utf-8'))
    time.sleep(2)   # Wait for grbl to initialize 
    s.flushInput()  # Flush startup text in serial input

    # Stream g-code to grbl
    
    print("Sending:", siirto.encode('utf-8'))
    s.write(siirto.encode()) # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" Vastaus" , grbl_out.strip())

    # Wait here until grbl is finished to close serial port and file.
    #raw_input("  Press <Enter> to exit and disable grbl.") 

    
    return

def kuvaAsento():
    # Open grbl serial port
    siirto = 'G90 X0 Y-174 Z0\n' #MUUTA NAMA
    string = '$#\n'
    #Wake up grbl
    s.write(string.encode('utf-8'))
    time.sleep(2)   # Wait for grbl to initialize 
    s.flushInput()  # Flush startup text in serial input

    # Stream g-code to grbl
    
    print("Sending:", siirto.encode('utf-8'))
    s.write(siirto.encode()) # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" Vastaus" , grbl_out.strip())

    # Wait here until grbl is finished to close serial port and file.
    #raw_input("  Press <Enter> to exit and disable grbl.") 


    
    return

def peliAsento():
    # Open grbl serial port
    siirto = 'G90 X0 Y-174 Z0\n' #MUUTA NAMA
    string = '$#\n'
    #Wake up grbl
    s.write(string.encode('utf-8'))
    time.sleep(2)   # Wait for grbl to initialize 
    s.flushInput()  # Flush startup text in serial input

    # Stream g-code to grbl
    
    print("Sending:", siirto.encode('utf-8'))
    s.write(siirto.encode()) # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" Vastaus" , grbl_out.strip())

    # Wait here until grbl is finished to close serial port and file.
    #raw_input("  Press <Enter> to exit and disable grbl.") 

    
    return

def painaNoppaa():
    # Open grbl serial port
    siirto = 'G90 X0 Y-174 Z0\n' #MUUTA NAMA
    string = '$#\n'
    #Wake up grbl
    s.write(string.encode('utf-8'))
    time.sleep(2)   # Wait for grbl to initialize 
    s.flushInput()  # Flush startup text in serial input

    # Stream g-code to grbl
    
    print("Sending:", siirto.encode('utf-8'))
    s.write(siirto.encode()) # Send g-code block to grbl
    s.flushInput()
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" Vastaus" , grbl_out.strip())

def siirra(i1,i2):
    xAlku = koordinaatit[i1[0]]
    yAlku = koordinaatit[i1[1]]
    xLoppu = koordinaatit[i2[0]]
    yLoppu = koordinaatit[i2[1]] 

    #Wake up grbl
    s.write("\r\n\r\n")
    time.sleep(2)   # Wait for grbl to initialize 
    s.flushInput()  # Flush startup text in serial input

    # Stream g-code to grbl
    
    print('Sending: $H ')
    s.write('$H') # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())

    # Wait here until grbl is finished to close serial port and file.
    #raw_input("  Press <Enter> to exit and disable grbl.") 

    return
 
openSerial()
homing()
kuvaAsento()
closeSerial()
