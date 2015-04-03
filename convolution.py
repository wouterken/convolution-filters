kernel = [
    [ 1,   0,  -1],
    [ 0,   0,  0],
    [ -1,   0,  1],
    ]


from Tkinter import *
import Image
import numpy
import ImageTk
import cStringIO
import struct
import math

base = Image.open('./house.png')
width, height = base.size
BASE_IMAGE = [struct.pack("BBB", 60, 60, 60)] * width * height
imgData = base.load()


div = 0
for lst in kernel:
    for val in lst:
        div += val
div = 1 if div is 0 else div

def to_pixel(col):
    return struct.pack("BBB", *col)

kw = len(kernel)
boundW = int(math.floor(kw / 2.))

kh = len(kernel[0])
boundH = int(math.floor(kh / 2.))

image = BASE_IMAGE[:]
bounds = [(x, y) for y in xrange(0, height) for x in xrange(0, width)]
bRange = [(i, j) for i in xrange(-boundW, boundW + 1) for j in xrange(-boundH , boundH + 1)]
pixels = {}
for tup in bounds:
        pixels[tup] = []
        r = 0
        g = 0
        b = 0
        for br in bRange:
            try:
                pixels[tup].append((br, imgData[tup[0] + br[0], tup[1] + br[1]]))
            except:
                pass
print "start"
for (x, y), neighbors in pixels.items():
    r = 0
    g = 0
    b = 0
    for (i, j), color in neighbors:
        mult = kernel[i][j]
        r += color[0] * mult
        g += color[1] * mult
        b += color[2] * mult
        pass
    col = (min(255, max(0, c/div)) for c in (r, g, b))
    image[y * width + x] = struct.pack("BBB", *col)
    pass

out = cStringIO.StringIO()
out.write("".join(image))

nImg = Image.fromstring("RGB", (width, height), out.getvalue())
root = Tk()
photo = ImageTk.PhotoImage(nImg)

label = Label(root, image=photo)
label.image = photo # keep a reference!
label.pack()

root.mainloop()
