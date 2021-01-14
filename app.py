from tkinter import *
from tkinter import font

import Pmw as Pmw
import numpy as np
from PIL import Image

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = '@%#*+=-:. '


def getAverageL(image):
    # get image as numpy array
    im = np.array(image)

    # get shape
    w, h = im.shape

    # get average
    return np.average(im.reshape(w * h))


def convertImageToAscii(fileName, cols, scale):
    # declare globals
    global gscale1, gscale2

    # open image and convert to grayscale
    image = Image.open(fileName).convert('L')

    # store dimensions
    W, H = image.size[0], image.size[1]
    print("Size of your initial image is %d x %d" % (W, H))

    # compute width of tile
    w = W / cols

    # compute tile height based on aspect ratio and scale
    h = w / scale

    # compute number of rows
    rows = int(H / h)

    print("Size of future ASCII-art will take %d cols and %d rows" % (cols, rows))
    # print("tile dims: %d x %d" % (w, h))

    # check if image size is too small
    if cols > W or rows > H:
        print("This image too small for this convertor!")
        exit(0)

        # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        # correct last tile
        if j == rows - 1:
            y2 = H

            # append an empty string
        aimg.append("")

        for i in range(cols):

            # crop image to tile
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            # correct last tile
            if i == cols - 1:
                x2 = W

                # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(getAverageL(img))

            # look up ascii char
            gsval = gscale2[int((avg * 9) / 255)]
            aimg[j] += gsval

    # return txt image
    return aimg


# main() function
def main():
    # create parser

    imgFile = file.get()

    scale = 0.43

    outFile = 'OPEN_ME.txt'

    cols = num_of_cols.get()

    print('Start converting the image...')
    # convert image to ascii txt
    aimg = convertImageToAscii(imgFile, cols, scale)

    # open file
    f = open(outFile, 'w')

    # write to file
    for row in aimg:
        # cleanup
        f.write(row + '\n')

    f.close()
    print("The finished ASCII-art is located in %s" % outFile)

    filename = outFile
    root = Tk()
    root.title('IMG to ASCII')
    root.geometry('1600x900')
    top = Frame(root)
    top.pack(side='top')
    text = Pmw.ScrolledText(top,
                            borderframe=0,
                            vscrollmode='dynamic',
                            hscrollmode='dynamic',
                            text_width=180,
                            text_height=45,
                            labelpos='n',
                            text_wrap='none',
                            )
    text.pack()
    text.insert('end', open(filename, 'r').read())
    Button(root, text="ОК", command=root.destroy).pack()
    root.mainloop()


root = Tk()
root.title("IMG в ASCII")

file = StringVar()
num_of_cols = IntVar()

file_label = Label(text="Введите название файла с картинкой:")
num_of_cols_label = Label(text="Введите количество столбцов для отображения ASCII-арта:")

file_label.grid(row=0, column=0, sticky="w")
num_of_cols_label.grid(row=1, column=0, sticky="w")

file_entry = Entry(textvariable=file)
num_of_cols_entry = Entry(textvariable=num_of_cols)

file_entry.grid(row=0, column=1, padx=5, pady=5)
num_of_cols_entry.grid(row=1, column=1, padx=5, pady=5)

exit = Button(text="Выход", command=root.destroy)
exit.grid(row=2, column=0, padx=3, pady=5, sticky="e")
message_button = Button(text="Конвертировать", command=main)
message_button.grid(row=2, column=1, padx=4, pady=5, sticky="e")

root.mainloop()
