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
    siirto = 'G90 X0 Y0 Z0\n' #MUUTA NAMA
    s = serial.Serial("COM9",115200)
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

    # Close file and serial port
    s.close()  

    
    return

def peliAsento():
    # Open grbl serial port
    siirto = 'G90 X0 Y0 Z0\n' #MUUTA NAMA
    s = serial.Serial("COM9",115200)
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

    # Close file and serial port
    s.close()  

    
    return

def painaNoppaa():
    import serial
    import time

    # Open grbl serial port
    s = serial.Serial('/dev/tty.usbmodem1811',115200)

    # Open g-code file
    f = open('grbl.gcode','r');

    # Wake up grbl
    s.write("\r\n\r\n")
    time.sleep(2)   # Wait for grbl to initialize 
    s.flushInput()  # Flush startup text in serial input

# Stream g-code to grbl
    for line in f:
        l = line.strip() # Strip all EOL characters for consistency
        print('Sending: ', l)
        s.write(l, '\n') # Send g-code block to grbl
        grbl_out = s.readline() # Wait for grbl response with carriage return
        print(' : ' , grbl_out.strip())

    # Wait here until grbl is finished to close serial port and file.
    raw_input("  Press <Enter> to exit and disable grbl.") 

    # Close file and serial port
    f.close()
    s.close()

def siirra(i1,i2):
    # Open grbl serial port
    s = serial.Serial('/dev/tty.usbmodem1811',115200)

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

    # Close file and serial port
    s.close()  

    return
 
homing()
