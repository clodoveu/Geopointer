#
# GeoPointer 
# V2 2018-07-23
# CADJ
#
# Controls two stepper motors 28BYJ-48 under driver ULN2003
#  and a laser diode to point at geographic coordinates in a wall map
#
# Map details: 
#   Blue Marble Next Generation: a true-color Earth dataset including seasonal dynamics from MODIS
#   Image corresponds to the month of August 2004
#   Projection: Geographic Plate Carrée, based on an equal latitude-longitude grid spacing
#   Datum: WGS84
#   Plot: 5000 x 2500 mm, in four vertical strips of 21600 x 43200 pixels
#         [1] 90N, 180W to 90S,  90W
#         [2] 90N,  90W to 90S,   0
#         [3] 90N,   0  to 90S,  90E
#         [4] 90N,  90E to 90S, 180E
#

import RPi.GPIO as GPIO
import time

# SETUP 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#  horizontal stepper motor
coilA1pin = 4
coilA2pin = 17
coilB1pin = 23
coilB2pin = 24
#  vertical stepper motor
coilC1pin = 27
coilC2pin = 22
coilD1pin = 5
coilD2pin = 6
#   laser trigger
laserPin = 26

motorDelay = 0.002 # seconds between stepper advancements

# GPIO SETUP
GPIO.setup(coilA1pin, GPIO.OUT)
GPIO.setup(coilA2pin, GPIO.OUT)
GPIO.setup(coilB1pin, GPIO.OUT)
GPIO.setup(coilB2pin, GPIO.OUT)
GPIO.setup(coilC1pin, GPIO.OUT)
GPIO.setup(coilC2pin, GPIO.OUT)
GPIO.setup(coilD1pin, GPIO.OUT)
GPIO.setup(coilD2pin, GPIO.OUT)
GPIO.setup(laserPin,  GPIO.OUT)

# sequencing for half-step 
stepCount = 8
seq = []
seq.append([1,0,0,0])
seq.append([1,1,0,0])
seq.append([0,1,0,0])
seq.append([0,1,1,0])
seq.append([0,0,1,0])
seq.append([0,0,1,1])
seq.append([0,0,0,1])
seq.append([1,0,0,1])
STEPX = 0 # global to indicate next step in sequence
STEPY = 0

def cleanup():
  GPIO.output(coilA1pin, False)
  GPIO.output(coilA2pin, False)
  GPIO.output(coilB1pin, False)
  GPIO.output(coilB2pin, False)
  GPIO.output(coilC1pin, False)
  GPIO.output(coilC2pin, False)
  GPIO.output(coilD1pin, False)
  GPIO.output(coilD2pin, False)
  GPIO.output(laserPin,  False)
    

def setStepX(s):
  GPIO.output(coilA1pin, seq[s][0])
  GPIO.output(coilA2pin, seq[s][1])
  GPIO.output(coilB1pin, seq[s][2])
  GPIO.output(coilB2pin, seq[s][3])

def setStepY(s):
  GPIO.output(coilC1pin, seq[s][0])
  GPIO.output(coilC2pin, seq[s][1])
  GPIO.output(coilD1pin, seq[s][2])
  GPIO.output(coilD2pin, seq[s][3])

def forwardX1():  
    global STEPX
    setStepX(STEPX)
    STEPX += 1
    if STEPX == stepCount:
        STEPX = 0
    time.sleep(motorDelay)

def backwardX1():
    global STEPX  
    STEPX -= 1
    if STEPX < 0:
        STEPX = stepCount - 1
    setStepX(STEPX)
    time.sleep(motorDelay)
    
def forwardY1():
    global STEPY  
    setStepY(STEPY)
    STEPY += 1
    if STEPY == stepCount:
        STEPY = 0
    time.sleep(motorDelay)

def backwardY1():
    global STEPY  
    STEPY -= 1
    if STEPY < 0:
        STEPY = stepCount - 1
    setStepY(STEPY)
    time.sleep(motorDelay)
    
def forwardX(steps):
    for i in range (0, steps):
        forwardX1()
        
def backwardX(steps):
    for i in range(0, steps):
        backwardX1()
  
def forwardY(steps):
    for i in range (0, steps):
        forwardY1()
        
def backwardY(steps):
    for i in range(0, steps):
        backwardY1()

def laserOn():
    GPIO.output(laserPin, True)

def laserOff():
    GPIO.output(laserPin, False)
        
# def coordsToSteps(?) # determina numero de passos dos motores para chegar a uma posicao
# def moveTo(absCoords):
# def move(deltaCoords):
# def laserOn():
# def laserOff():
# def moveSeq(coordList):
# def calibrate():
# def calibrateOrigin():
# def calibrateExtremities():
  
def main():
# test section while main() is not written
    while True:
        laserOn()
        steps = input("How many steps forward in X? ")
        if int(steps) == 0:
            break
        forwardX(int(steps))
        steps = input("How many steps backwards in X? ")
        backwardX(int(steps))
        steps = input("How many steps forward in Y? ")
        forwardY(int(steps))
        steps = input("How many steps backwards in Y? ")
        backwardY(int(steps))

    laserOff()
    cleanup()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
