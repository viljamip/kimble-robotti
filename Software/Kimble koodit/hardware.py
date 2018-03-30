import serial
import time

koordinaatit = [(-3.12,-139.7),(-9.08,-139.4),(-15.4,-135.2),(-21.88,-132.0),(-28.4,-135.1),(-34.6,-138.9),(-40.72,-138.7),(-46.88,-138.4),(-52.96,-138.5),(-59.48,-134.4),(-65.88,-131.3),(-72.36,-134.5),(-78.68,-138.4),(-84.8,-138.3),(-91.0,-138.2),(-97.2,-138.3),(-103.48,-134.3),(-109.88,-131.3),(-116.4,-134.3),(-122.8,-138.7),(-128.88,-138.7),(-135.08,-138.9),(-141.28,-138.8),(-147.68,-134.9),(-154.16,-131.7),(-160.56,-135.0),(-166.76,-139.2),(-172.96,-139.2),(-175.96,-125.1),(-175.96,-106.6),(-175.96,-87.7),(-175.96,-69.1),(5.64,-158.3),(2.040,-158.1),(-1.68,-158.0),(-5.36,-157.9),(-38.28,-157.8),(-41.96,-157.6),(-45.76,-157.6),(-49.48,-157.4),(-82.36,-157.2),(-86.08,-157.4),(-89.76,-157.4),(-93.56,-157.2),(-126.36,-157.2),(-130.16,-157.4),(-133.88,-157.4),(-137.56,-157.3),(-132.16,-124.4),(-132.16,-105.7),(-132.16,-87.2),(-132.16,-68.5),(-43.76,-124.6),(-43.76,-105.9),(-43.76,-87.2),(-43.76,-68.5),(-87.96,-124.4),(-87.96,-105.8),(-87.96,-86.8),(-87.96,-68.2)]


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

    string = '$#\n'
    #Wake up grbl
    s.write(string.encode('utf-8'))
    time.sleep(2)   # Wait for grbl to initialize 
    s.flushInput()  # Flush startup text in serial input

    # Ajetaan nopan p‰‰lle
    siirto = 'G90 Y0 Z-1\n' #MUUTA NAMA    
    print("Sending:", siirto.encode('utf-8'))
    s.write(siirto.encode()) # Send g-code block to grbl
    s.flushInput()
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" Vastaus" , grbl_out.strip())
    
    #painetaan noppaa
    siirto = 'G90  Z-26\n'
    print("Sending:", siirto.encode('utf-8'))
    s.write(siirto.encode()) # Send g-code block to grbl
    s.flushInput()
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" Vastaus" , grbl_out.strip())


def siirra(i1,i2):
    print(koordinaatit[i1][0])
    xAlku = koordinaatit[i1][0]
    yAlku = koordinaatit[i1][1]
    xLoppu = koordinaatit[i2][0]
    yLoppu = koordinaatit[i2][1] 

    #'{1} {0}'.format('one', 'two')

    #Wake up grbl
    #s.write(("\r\n\r\n").encode())
    #time.sleep(2)   # Wait for grbl to initialize 
    #s.flushInput()  # Flush startup text in serial input
    zYlos = 'G90 Z-1\n'
    s.write(zYlos.encode('utf-8'))
    grbl_out = s.readline() # Wait for grbl response with carriage return
    # Stream g-code to grbl
    nappaa = 'G90 X{} Y{}\n'.format(xAlku, yAlku)
    laske  = 'G90 X{} Y{}\n'.format(xLoppu, yLoppu)
    
    #Haetaan nappi
    print('Sending:', nappaa)
    s.write(nappaa.encode('utf-8')) # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" : ", grbl_out.strip())
    s.write('G90 Z-32\n'.encode('utf-8'))
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" : ", grbl_out.strip())
    s.write('M8\n'.encode('utf-8'))
    grbl_out = s.readline()
    print(" : ", grbl_out.strip())
    s.write('G90 Z-1\n'.encode('utf-8'))
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" : ", grbl_out.strip())
    
    #pudotetaan nappi
    print('Sending:', laske)
    s.write(laske.encode('utf-8')) # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    s.write('G90 Z-32\n'.encode('utf-8'))
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" : ", grbl_out.strip())
    s.write('M9\n'.encode('utf-8'))
    grbl_out = s.readline()
    print(" : ", grbl_out.strip())
    s.write('G90 Z-1\n'.encode('utf-8'))
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(" : ", grbl_out.strip())

    # Wait here until grbl is finished to close serial port and file.
    #raw_input("  Press <Enter> to exit and disable grbl.") 

    return
 
openSerial()
homing()
siirra(0,9)
closeSerial()
