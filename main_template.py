from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, ImageOps
import PIL.Image
import os
from pre_processing import *
import cv2


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        root.title("Processamento Digital de Imagem")

        self.titulo = Label(
            text="Seleciona a imagem clicando no botao abaixo",
            bg="light gray",
        )
        self.titulo["font"] = ("Calibri", "14", "bold")
        self.titulo.grid(row=0, column=1, pady=5)

        self.selimg = Button(
            master,
            text="Abrir Imagem",
            command=self.open_img,
            relief=RAISED,
            fg="black",
            bg="light blue",
            borderwidth=1,
            padx=30,
        )
        self.selimg.grid(row=1, column=1)

        self.imagepathdisplay = Entry(
            master,
            text="Caminho para imagem",
            fg="gray",
            width=40,
            font=("Consolas 12"),
            borderwidth=3,
        )
        self.imagepathdisplay.insert(0, "Nenhuma imagem selecionada")
        self.imagepathdisplay.configure(state="readonly")
        self.imagepathdisplay.grid(row=2, column=1)

        self.imglabel = Label(
            master,
            text="Pré visualização",
            font=("Consolas 10"),
            pady=5,
            bg="light gray",
        )
        self.imglabel.grid(row=3, column=1)

        self.img = ImageTk.PhotoImage(
            PIL.Image.open("defimg.png").resize((700, 700), PIL.Image.ANTIALIAS)
        )
        self.imgpanel = Label(image=self.img)
        self.imgpanel.grid(row=4, column=1)

        self.startprocess = Button(
            master,
            text="Começar",
            command=self.openNewWindow,
            relief=RAISED,
            fg="black",
            bg="light blue",
            borderwidth=1,
            padx=30,
        )
        self.startprocess.grid(row=5, column=5, columnspan=1)

        self.closeprocess = Button(
            master,
            text="Sair",
            command=root.destroy,
            relief=RAISED,
            fg="black",
            bg="#ed5959",
            borderwidth=1,
            padx=30,
        )
        self.closeprocess.grid(row=5, column=0, columnspan=1)

        self.titulo = Label(
            text="Resultado do processamento",
            bg="light gray",
        )
        self.titulo["font"] = ("Calibri", "14", "bold")
        self.titulo.grid(row=0, column=4, pady=5)

        self.img_result = ImageTk.PhotoImage(
            PIL.Image.open("defimg.png").resize((700, 700), PIL.Image.ANTIALIAS)
        )
        self.imgpanel_2 = Label(image=self.img_result)
        self.imgpanel_2.grid(row=4, column=4)

    def open_img(self):
        try:
            filename = filedialog.askopenfilename(title="abrir")
        except:
            return
        try:
            img = PIL.Image.open(filename)
        except:
            messagebox.showerror("ERRO!!", "Nenhuma imagem selecionada")
            return
        self.selectedimagepath = filename
        self.imagepathdisplay.configure(state="normal")
        self.imagepathdisplay.configure(fg="gray")
        self.imagepathdisplay.delete(0, END)
        self.imagepathdisplay.insert(0, filename)
        self.imagepathdisplay.configure(state="readonly")
        self.imagepath = filename
        # img = cv2.imread(self.imagepath)
        # transform_image = PIL.Image.fromarray(img)
        # transform_image = ImageOps.grayscale(transform_image)
        # width, height = img.size
        img = img.resize((700, 700), PIL.Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.imgpanel.configure(image=img)
        self.img = img

    def openNewWindow(self):
        # newWindow = Toplevel(self)
        # newWindow.title("Pré-Processamento")
        # newWindow.minsize(720, 700)

        # extractWindow = Toplevel(self)
        # extractWindow.title("Extracao de Caracteristica")
        # extractWindow.minsize(720, 700)

        result_image, opencv = PreProcessing.pre_process(self.imagepath)
        transform_image = PIL.Image.fromarray(result_image)
        # transform_image = ImageOps.grayscale(transform_image)
        self.imagepreprocessing = ImageTk.PhotoImage(transform_image)
        # Label(
        #     newWindow,
        #     text="Pre processamento",
        #     bg="light gray",
        # ).grid(row=0, column=0)
        # Label(newWindow, image=self.imagepreprocessing).grid(row=1, column=0)

        segimage = PreProcessing.segmentationProcess(result_image, opencv)
        transform_image = PIL.Image.fromarray(segimage)
        self.imageseg = ImageTk.PhotoImage(transform_image)
        # Label(
        #     newWindow,
        #     text="Segmentacao",
        #     bg="light gray",
        # ).grid(row=0, column=1)
        # Label(newWindow, image=self.imageseg).grid(row=1, column=1)

        ######
        eqimage = PreProcessing.featureExtration(segimage)
        transform_image = PIL.Image.fromarray(eqimage)
        self.imageeq = ImageTk.PhotoImage(transform_image)
        # Label(
        #     extractWindow,
        #     text="Extração caracteristica",
        #     bg="light gray",
        # ).grid(row=0, column=0)
        # Label(extractWindow, image=self.imageeq).grid(row=1, column=0)

        cannyimage = PreProcessing.edgeDetection(eqimage, self.imagepath)
        transform_image = PIL.Image.fromarray(cannyimage)
        self.img_result = ImageTk.PhotoImage(transform_image)
        self.imgpanel_2.configure(image=self.img_result)
        # Label(
        #     extractWindow,
        #     text="Canny",
        #     bg="light gray",
        # ).grid(row=0, column=1)
        # Label(extractWindow, image=self.cannyimage).grid(row=1, column=1)


root = Tk()
# root.minsize(720, 860)
w = 1620  # width for the Tk root
h = 860  # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))
root.configure(bg="light gray")
Application(root)
root.mainloop()
