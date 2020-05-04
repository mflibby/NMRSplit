from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


window = Tk()

window.title("NMR Splitting")

window.geometry('300x120')

required_vals = ['Hcount', 'Js', 'Jcounts', 'Resolution']

rows = 0
objects = []

for i in required_vals:
    temp = Entry(window, width = 14)
    temp.grid(column = 1, row=rows)
    temp_lbl = Label(window, text = i)
    temp_lbl.grid(column=0, row=rows)

    objects.append(temp)
    rows += 1

def css_to_list(string):
    temp = ""
    stringlist = []
    for i in enumerate(string):
        if i[1]!=',':
            temp += i[1]
        else:
            stringlist.append(float(temp))
            temp = ""
        if i[0]==len(string)-1:
            stringlist.append(float(temp))
    return stringlist

def gaussian(x, mean, amplitude, standard_deviation):
    return amplitude * np.exp( - ((x - mean)**2 / (2*standard_deviation**2)))

def clicked():
    Hcount = float(objects[0].get())
    Jsstring = objects[1].get()
    Jcountstring = objects[2].get()
    resolution = float(objects[3].get())

    Js = css_to_list(Jsstring)
    Jcounts = css_to_list(Jcountstring)
    Jcounts = [int(i) for i in Jcounts]

    #text = "Rs = " + str(Rs) + "\n" + "Rg = " + str(Rg) + "\n" +"Rd = " + str(Rd) + "\n" + "Cs = " + str(Cs) + "\n" +"Cg = " + str(Cg) + "\n" + "Cd = " + str(Cd) + "\n"
    #messagebox.showinfo('BJT',Js)

    splits = []
    for i in range(len(Js)):
        for j in range(Jcounts[i]):
            splits.append(Js[i])
    splits.sort()

    peaks = [[0]]
    for i in splits:
        newlist = []
        for j in peaks[-1]:
            newhigh = j + i/2
            newlow = j - i/2
            newlist.append(newlow)
            newlist.append(newhigh)
        peaks.append(newlist)
    centers = peaks[-1]

    gaussians = []
    std = resolution
    plotrange = np.arange(min(centers) - (std*5),max(centers) + (std*5), std*0.25)
    amp = Hcount / (len(centers)*std*np.sqrt(2*np.pi))
    for i in centers:
        y = gaussian(plotrange, i, amp, std)
        gaussians.append(y)

    summedgaussians = []
    for x in range(len(plotrange)):
        summedy = 0
        for i in range(len(gaussians)):
            summedy = summedy + gaussians[i][x]
        summedgaussians.append(summedy)

    plt.figure(figsize=(17,10))
    plt.plot(plotrange,summedgaussians)
    plt.show()

    #fig = Figure(figsize=(5, 4), dpi=100)
    #fig.add_subplot(111).plot(plotrange,summedgaussians)

    #canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
    #canvas.draw()
    #canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    #toolbar = NavigationToolbar2Tk(canvas, window)
    #toolbar.update()
    #canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

btn = Button(window, text='Click', command=clicked, width =20)

btn.grid(column=0,row=10, columnspan = 3, padx=10)

#def _quit():
#    window.quit()     # stops mainloop
#    window.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

#button = Button(master=window, text="Quit", command=_quit)
#button.grid(column=0,row=11, columnspan = 3, padx=10)

window.mainloop()
