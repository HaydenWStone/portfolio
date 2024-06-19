"""
This code enables a Kasa smart plug to cycle and send morse code messages
"""

import asyncio
import kasa
import time

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', ' ':' ',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

#Set plug address here
lamp = kasa.SmartPlug("IP HERE")

#On/off function
async def lightswitch():
    await lamp.update()
    if lamp.is_on:
        await lamp.turn_off()
    if lamp.is_off:
        await lamp.turn_on()

#Morse dash
def dash():
    asyncio.run(lightswitch())
    time.sleep(1.5)
    asyncio.run(lightswitch())
    time.sleep(.5)

#Morse dot
def dot():
    asyncio.run(lightswitch())
    time.sleep(.5)
    asyncio.run(lightswitch())
    time.sleep(.5)

#Space
def space():
    time.sleep(2)

#Main message function
def send_message():
    message = input("What would you like to transmit?\n")
    char_list = list(message)
    morse_list = []
    for char in char_list:
        morse_list.append(MORSE_CODE_DICT[char.upper()])

    asyncio.run(lamp.turn_off())
    time.sleep(3)

    for char in morse_list:
        for subchar in char:
            if subchar == ".":
                dot()
            if subchar == "-":
                dash()
            if subchar == ' ':
                space()
        time.sleep(3)

#Driver
send_message()

