"""
This script creates a converter to translate between decimal degrees and degrees/minutes/seconds of latitude and longitude
"""

import tkinter
import math

#Initalize tkinter window
window = tkinter.Tk()
window.title("Lat/Long Converter")
window.minsize(100,100)
window.config(padx=20,pady=20)

#Create entry box
box = tkinter.Entry()
box.config(width=10)
box.grid(row=2,column=2)

#Create label
label_one = tkinter.Label(text="Decimal Degrees")
label_one.grid(row=3,column=2)

#Decimal degree to DMS converter formula
def convert():
    dec_degrees = float(box.get())
    degrees = math.floor(dec_degrees)
    dec_minutes = (dec_degrees - degrees) * 60
    minutes = math.floor(dec_minutes)
    minutes_round = round(minutes)
    epsilon = 1e-10
    seconds = (dec_degrees - degrees - minutes/60 + epsilon) * 3600
    seconds_round = round(seconds,1)
    output.config(text=f"{degrees} degrees, {minutes_round} minutes, {seconds_round} seconds")

#Create label
isequal = tkinter.Label(text="are equal to")
isequal.grid(row=5,column=2)

#Create output
output = tkinter.Label(text="0 degrees, 0 minutes, 0 seconds")
output.grid(row=6,column=2)

#Create button
button = tkinter.Button(text="Convert",command=convert)
button.grid(row=4,column=2)

#Spacer
middle = tkinter.Label(text="\n\n\n")
middle.grid(row=7,column=2)

#Create entry box
box_two = tkinter.Entry()
box_two.config(width=10)
box_two.grid(row=9,column=2)

#Create label
label_two = tkinter.Label(text="DMS (Seperate with spaces)")
label_two.grid(row=10,column=2)

#DMS to decimal degree converter forumla
def convert():
    input_str = box_two.get().split()
    degrees = float(input_str[0])
    minutes = float(input_str[1])
    seconds = float(input_str[2])
    decimal_degrees = round(degrees + minutes/60 + seconds/3600,4)
    output_two.config(text=f"{decimal_degrees} decimal degrees")

#Create label
isequal_two = tkinter.Label(text="are equal to")
isequal_two.grid(row=12,column=2)

#Create output
output_two = tkinter.Label(text="0 decimal degrees")
output_two.grid(row=13,column=2)

#Create button
button_two = tkinter.Button(text="Convert",command=convert)
button_two.grid(row=11,column=2)

#Run main loop
window.mainloop()
