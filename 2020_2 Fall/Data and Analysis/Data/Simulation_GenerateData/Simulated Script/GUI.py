import tkinter as tk

root = tk.Tk()

greeting = tk.Label(text='Creating Simulation Dataset', width = 35)
label1 = tk.Label(text='Enter alpha')
entry1 = tk.Entry()
entry1.insert(0, '0')
button = tk.Button(text = 'click')

greeting.pack()
label1.pack()
entry1.pack()
button.pack()
root.mainloop()