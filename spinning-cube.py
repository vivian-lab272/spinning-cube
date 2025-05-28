import math
import time
import os
import sys

A = B = C = 0

cubeWidth = 30
width, height = 100, 45
zBuffer = [0] * (width * height)
buffer = [' '] * (width * height)
backgroundASCIICode = '.'
distanceFromCam = 100
horizontalOffset = 0
K1 = 40

incrementSpeed = 0.6

def calculateX(i, j, k):
    return j * math.sin(A) * math.sin(B) * math.cos(C) - k * math.cos(A) * math.sin(B) * math.cos(C) + \
           j * math.cos(A) * math.sin(C) + k * math.sin(A) * math.sin(C) + i * math.cos(B) * math.cos(C)

def calculateY(i, j, k):
    return j * math.cos(A) * math.cos(C) + k * math.sin(A) * math.cos(C) - \
           j * math.sin(A) * math.sin(B) * math.sin(C) + k * math.cos(A) * math.sin(B) * math.sin(C) - \
           i * math.cos(B) * math.sin(C)

def calculateZ(i, j, k):
    return k * math.cos(A) * math.cos(B) - j * math.sin(A) * math.cos(B) + i * math.sin(B)

def calculateForSurface(cubeX, cubeY, cubeZ, ch):
    global x, y, z, ooz, xp, yp, idx
    x = calculateX(cubeX, cubeY, cubeZ)
    y = calculateY(cubeX, cubeY, cubeZ)
    z = calculateZ(cubeX, cubeY, cubeZ) + distanceFromCam
    ooz = 1 / z
    xp = int(width / 2 + horizontalOffset + K1 * ooz * x * 2)
    yp = int(height / 2 + K1 * ooz * y)
    idx = xp + yp * width
    if 0 <= idx < width * height:
        if ooz > zBuffer[idx]:
            zBuffer[idx] = ooz
            buffer[idx] = ch

def renderCube(cubeWidth, offset, chars):
    global horizontalOffset
    horizontalOffset = offset * cubeWidth
    for cubeX in frange(-cubeWidth, cubeWidth, incrementSpeed):
        for cubeY in frange(-cubeWidth, cubeWidth, incrementSpeed):
            calculateForSurface(cubeX, cubeY, -cubeWidth, chars[0])
            calculateForSurface(cubeWidth, cubeY, cubeX, chars[1])
            calculateForSurface(-cubeWidth, cubeY, -cubeX, chars[2])
            calculateForSurface(-cubeX, cubeY, cubeWidth, chars[3])
            calculateForSurface(cubeX, -cubeWidth, -cubeY, chars[4])
            calculateForSurface(cubeX, cubeWidth, cubeY, chars[5])

def frange(start, stop, step):
    while start < stop:
        yield start
        start += step

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        buffer = [backgroundASCIICode] * (width * height)
        zBuffer = [0] * (width * height)

        renderCube(20, -2, ['@', '$', '~', '#', ';', '+'])
        renderCube(10, 1, ['@', '$', '~', '#', ';', '+'])
        renderCube(5, 8, ['@', '$', '~', '#', ';', '+'])

        print("\x1b[H", end="")
        for k in range(width * height):
            sys.stdout.write(buffer[k] if k % width else '\n')

        A += 0.05
        B += 0.05
        C += 0.01
        time.sleep(0.015)