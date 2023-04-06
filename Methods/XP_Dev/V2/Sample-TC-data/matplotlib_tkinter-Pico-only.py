import matplotlib # import matplotlib first
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter
import numpy
import pandas

window = tkinter.Tk()
window.wm_title("Sample production overview")
window.state('zoomed')
fig = matplotlib.figure.Figure(figsize=(8, 6), dpi=100)
a = fig.add_subplot(111)




df = pandas.read_csv('RAW/10-02/10-02-pico-data-update.csv')

# Def values

time = df.values[:,0]
#TA =  df.values[:,1]
#TB =  df.values[:,2]
TC1 =  df.values[:,6]
TC5 =  df.values[:,7]
TC6 =  df.values[:,8]




a.set_title("Sample production (date)")
a.set_xlabel("time in seconds")
a.set_ylabel("Temperature (K)")

a.plot(time, TC1, '-', label = "TC 1 IN bottom")
a.plot(time, TC5, 'r-', label = "TC 2 IN top")
a.plot(time, TB, 'g-', label = "TC 3 OUT")
a.plot(time, TC6, 'b-', label = "Flying")


canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


toolbar = NavigationToolbar2TkAgg(canvas,window)
toolbar.update()
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def _quit():
    window.quit()
    window.destroy()
    
button = tkinter.Button(master=window, text='Quit', command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()

