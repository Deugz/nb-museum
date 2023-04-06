import matplotlib # import matplotlib first
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter
import numpy
import pandas

window = tkinter.Tk()
window.wm_title("Sample production overview")
window.state('zoomed')
fig = matplotlib.figure.Figure(figsize=(8, 6), dpi=100)
a = fig.add_subplot(111)




df = pandas.read_csv('Merged/06-02-TC-Merged.csv')

# Def values

time = df.values[:,0]
TA =  df.values[:,1]
TB =  df.values[:,2]
TC1 =  df.values[:,8]
TC5 =  df.values[:,9]
TC6 =  df.values[:,10]
TC4 =  df.values[:,11]



a.set_title("Sample production (date)")
a.set_xlabel("time in seconds")
a.set_ylabel("Temperature (K)")

a.plot(time, TC1, 'm-', label = "TC 1 ")
a.plot(time, TC5, 'g-', label = "TC 2 ")
#a.plot(time, TA, 'c-', label = "TC A ")
#a.plot(time, TB, 'b-', label = "TC B ")
a.plot(time, TC6, 'y-', label = "TC 4")
a.plot(time, TC4, 'r-', label = "TC 3")

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


toolbar = NavigationToolbar2Tk(canvas,window)
toolbar.update()
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def _quit():
    window.quit()
    window.destroy()
    
button = tkinter.Button(master=window, text='Quit', command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()

