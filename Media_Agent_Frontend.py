import sys
import os
from Media_Agent_Backend import *
import tkinter as tk
from tkinter import simpledialog

def execute_check():
    result = checkCredentials ("urn:VATIN:"+entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get())

    emergingWindow = tk.Tk()
    emergingWindow.title("Result")
    labelRES = tk.Label(emergingWindow, text= result, font = "Arial 12")
    labelRES.pack()
    buttonRES = tk.Button(emergingWindow, text='OK', command=emergingWindow.quit)
    buttonRES.pack()


#generate a dict that relates the video data with the isan identifier imitating a Database with this information
videosDict = {}
videosDict['sample01.mp4']= 'isan:aa111aa'
videosDict['sample02.mov']= 'isan:bb222bb'
videosDict['sample03.mp4']= 'isan:cc333cc'

#create a list of the video options available imitating a Database
DeliveryModes = ['Linear', 'NonLinear', 'Broadcasting']
Means = ['None', 'Satellite', 'Internet']
Countries = ['ES', 'EN', 'IT']
Languages = ['es', 'cat', 'eng']

#ES11111111111
#ES22222222222
#EN33333333333

tuples = videosDict.keys()
list = list(tuples)

root = tk.Tk()
root.title("Introduce Request specifications")
#root.geometry("400x300")

label1 = tk.Label(root, text="User ID").grid(row=0)
label3 = tk.Label(root, text="Video to play").grid(row=1)
label3 = tk.Label(root, text="Delivery Mode").grid(row=2)
label3 = tk.Label(root, text="Broadcasting Mean").grid(row=3)
label3 = tk.Label(root, text="Broadcasting Country").grid(row=4)
label3 = tk.Label(root, text="Video Language").grid(row=5)
label2 = tk.Label(root, text="").grid(row=6)

entry1 = tk.Entry(root, font="Arial 10")
entry1.grid(row=0, column=1)
entry2 = tk.StringVar(root)
entry2.set(list[0]) #default value
entry3 = tk.StringVar(root)
entry3.set(DeliveryModes[0]) #default value
entry4 = tk.StringVar(root)
entry4.set(Means[0]) #default value
entry5 = tk.StringVar(root)
entry5.set(Countries[0]) #default value
entry6 = tk.StringVar(root)
entry6.set(Languages[0]) #default value

menu1 = tk.OptionMenu(root, entry2, *list).grid(row=1, column= 1)
menu2 = tk.OptionMenu(root, entry3, *DeliveryModes).grid(row=2, column= 1)
menu3 = tk.OptionMenu(root, entry4, *Means).grid(row=3, column= 1)
menu4 = tk.OptionMenu(root, entry5, *Countries).grid(row=4, column= 1)
menu5 = tk.OptionMenu(root, entry6, *Languages).grid(row=5, column= 1)

button1 = tk.Button(root, text='Cancel', command=root.quit, bg="red").grid(row=7, column= 0)
button2 = tk.Button(root, text='OK', command=execute_check, bg="cyan").grid(row=7, column= 1)
#button2 = tk.Button(root, text='OK', command= lambda: show_entry_fields(arguments))

tk.mainloop()