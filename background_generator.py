import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter.filedialog import asksaveasfilename
import matplotlib.pyplot as plt
import numpy as np
import math

matplotlib.use('TkAgg')


def expr(x, y, nnn):
    L = 0.1
    i = np.arange(nnn) + 1
    c = 1
    omega = 100
    D = np.zeros([np.size(x), nnn])
    [X, I] = np.meshgrid(x, i)
    [Y, I] = np.meshgrid(y, i)
    D = np.sqrt((L ** 2) + (X - 2 * np.cos(2 * math.pi * I / nnn)) ** 2 + (Y - 2 * np.sin(2 * math.pi * I / nnn)) ** 2)
    a = 1j / D
    gamma = np.exp((-1j * D * omega) / c)
    return np.sum(gamma * a, 0)


def generatePattern(nnn, ii, mag):
    d = 6 * mag * ii
    l = 120 * mag
    R1 = np.arange(l)
    R2 = np.arange(l)
    A1, A2 = np.meshgrid(R1, R2)
    S = np.exp(1j * (A1 + A2))
    f1, f2 = np.meshgrid(np.linspace(-d, d, l), np.linspace(-d, d, l))
    f = np.zeros((l, l), dtype=np.complex_)
    A = np.zeros((l, l), dtype=np.complex_)

    for i in range(np.size(R1)):
        f[i, :] = expr(f1[i, :], f2[i, :], nnn)

    AA = np.exp(1j * (A1 + A2))
    s = (AA * mag * ii * f) / nnn
    X = np.absolute(np.fft.fft2(s))
    s = np.absolute(s)
    return X * (255.0 / X.max())  # , s*(255.0/s.max())


def drawPattern(pinhole_number, iterations, contrast):  # quality 1 lowest, 5 highest
    nnn, mag, ii = pinhole_number, 6, iterations
    X = generatePattern(pinhole_number, iterations, mag)
    XX = np.concatenate((X, np.flip(X, axis=1)), axis=1)
    XX = np.concatenate((XX, np.flip(XX, axis=0)), axis=0)
    XX = np.concatenate((XX, np.flip(XX, axis=0)), axis=0)
    return XX


fields = ('Pinhole Number (1 - 12)', 'Iterations (0 - 1000)', 'Contrast (0 - 255)')


def __init__(self, window):
    self.window = window
    self.box = Entry(window)
    self.button = Button(window, text="check", command=self.Generate_Image())
    self.box.pack()
    self.button.pack()


def Generate_Image(entries):
    nnn = int(entries['Pinhole Number (1 - 12)'].get())
    ii = float(entries['Iterations (0 - 1000)'].get())
    contrast = int(entries['Contrast (0 - 255)'].get())
    XX = drawPattern(nnn, ii, contrast)
    width, height = np.shape(XX)
    fig = plt.figure(figsize=(15, 30))
    im = plt.imshow(XX, interpolation='Gaussian', cmap='gray', vmin=0, vmax=contrast)
    ax = plt.gca()
    ax.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()
    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"), ("All Files", "*.*")),
                          defaultextension='.png', title="Window-2")
    fig.savefig(a, bbox_inches='tight', pad_inches=0, dpi=397)


def makeform(root, fields):
    entries = {}
    for field in fields:
        print(field)
        row = Frame(root)
        lab = Label(row, width=22, text=field + ": ", anchor='w')
        ent = Entry(row)
        ent.insert(0, "0")
        row.pack(side=TOP,
                 fill=X,
                 padx=5,
                 pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT,
                 expand=YES,
                 fill=X)
        entries[field] = ent
    return entries


root = Tk()
ents = makeform(root, fields)
b1 = Button(root, text='Generate_Image',
            command=(lambda e=ents: Generate_Image(e)))
b1.pack(side=LEFT, padx=5, pady=5)
b3 = Button(root, text='Quit', command=root.quit)
b3.pack(side=LEFT, padx=5, pady=5)
root.mainloop()
