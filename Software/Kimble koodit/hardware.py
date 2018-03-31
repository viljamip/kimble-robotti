import serial
import time
import kamera

koordinaatit = [(-3.12,-139.7),(-9.08,-139.4),(-15.4,-135.2),(-21.88,-132.0),(-28.4,-135.1),(-34.6,-138.9),(-40.72,-138.7),(-46.88,-138.4),(-52.96,-138.5),(-59.48,-134.4),(-65.88,-131.3),(-72.36,-134.5),(-78.68,-138.4),(-84.8,-138.3),(-91.0,-138.2),(-97.2,-138.3),(-103.48,-134.3),(-109.88,-131.3),(-116.4,-134.3),(-122.8,-138.7),(-128.88,-138.7),(-135.08,-138.9),(-141.28,-138.8),(-147.68,-134.9),(-154.16,-131.7),(-160.56,-135.0),(-166.76,-139.2),(-172.96,-139.2),(-175.96,-125.1),(-175.96,-106.6),(-175.96,-87.7),(-175.96,-69.1),(5.64,-158.3),(2.040,-158.1),(-1.68,-158.0),(-5.36,-157.9),(-38.28,-157.8),(-41.96,-157.6),(-45.76,-157.6),(-49.48,-157.4),(-82.36,-157.2),(-86.08,-157.4),(-89.76,-157.4),(-93.56,-157.2),(-126.36,-157.2),(-130.16,-157.4),(-133.88,-157.4),(-137.56,-157.3),(-132.16,-124.4),(-132.16,-105.7),(-132.16,-87.2),(-132.16,-68.5),(-43.76,-124.6),(-43.76,-105.9),(-43.76,-87.2),(-43.76,-68.5),(-87.96,-124.4),(-87.96,-105.8),(-87.96,-86.8),(-87.96,-68.2)]



def openSerial():
    global s
    s = serial.Serial("/dev/cu.usbserial-DN03VXGO",115200) #/dev/cu.usbserial-DN03VXGO 
    return 1

def closeSerial():
    s.close()
    

def homing():
    # Open grbl serial port
    homing = '$H'
    wakeupcall = '?'
    #Wake up grbl
    lahetaGcode(wakeupcall)
    time.sleep(1)   # Wait for grbl to initialize 
    lahetaGcode(homing)
    odotaPysahtymista()
    return

def kuvaAsento():
    asento = 'G1 X22 Y-174 Z-1 F8000' 
    lahetaGcode(asento)
    return 1

def peliAsento():
    asento = 'G1 X0 Y-174 Z-1 F8000'
    lahetaGcode(asento)
    valo(True)
    return

def painaNoppaa():
    # Ajetaan nopan paalle
    siirto = 'G1 Y0 Z-1 F8000'
    lahetaGcode(siirto)  
    
    #painetaan noppaa
    siirto = 'G1  Z-20 F4000'
    lahetaGcode(siirto)
    siirto = 'G1  Z-27 F1000'
    lahetaGcode(siirto)
    siirto = 'G1  Z-1 F4000'
    lahetaGcode(siirto)
    silmaluku = kamera.nopanSilmaluku()
    return silmaluku

def lahetaGcode(koodi):
    print("lähetetään: {0}".format(koodi))
    s.write('{0}\n'.format(koodi).encode('utf-8'))
    s.flushInput()
    grbl_out = s.readline()
    print(" Vastaus" , grbl_out.strip())
    
def odotaPysahtymista():
    valmis = False
    count = 0
    while(not valmis):
        time.sleep(0.1)
        s.write('?'.encode('utf-8'))
        s.flushInput()
        grbl_out = s.readline()
        valmis = "Idle" in str(grbl_out)
        if not valmis:
            count = count + 1
    print('odotuksen wait-määrä {0}'.format(count))
    if count>0:
        time.sleep(1)


def siirra(i1,i2):
    print(koordinaatit[i1][0])
    xAlku = koordinaatit[i1][0]
    yAlku = koordinaatit[i1][1]
    xLoppu = koordinaatit[i2][0]
    yLoppu = koordinaatit[i2][1] 

    zYlos = 'G1 Z-1 F4000'
    lahetaGcode(zYlos)

    nappaa = 'G1 X{} Y{} F8000'.format(xAlku, yAlku)
    laske  = 'G1 X{} Y{} F8000'.format(xLoppu, yLoppu)
    
    #Haetaan nappi
    lahetaGcode(nappaa)
    lahetaGcode('G1 Z-32 F4000')
    lahetaGcode('M8')
    lahetaGcode('G1 Z-1 F4000')
    
    #pudotetaan nappi
    lahetaGcode(laske)
    lahetaGcode('G1 Z-32 F4000')
    lahetaGcode('M9')
    lahetaGcode('G1 Z-1 F4000')
    
    return
 
def valo(paalla):
    if paalla:
            lahetaGcode('M3 S1000')
    else:
            lahetaGcode('M5')
    return

#openSerial()
#homing()
#valo(True)
#painaNoppaa()
#valo(False)
#siirra(31, 49)
#closeSerial()
