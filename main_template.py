from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk
import PIL.Image
import os


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        root.title("Processamento Digital de Imagem")

        self.titulo = Label(
            text="Seleciona a imagem clicando no botao abaixo",
            bg="light gray",
        )
        self.titulo["font"] = ("Calibri", "14", "bold")
        self.titulo.pack(pady=5)

        self.selimg = Button(
            text="Abrir Imagem",
            command=self.open_img,
            relief=RAISED,
            fg="black",
            bg="light blue",
            borderwidth=1,
            padx=30,
        )
        self.selimg.pack()

        self.imagepathdisplay = Entry(
            text="Caminho para imagem",
            fg="gray",
            width=40,
            font=("Consolas 12"),
            borderwidth=3,
        )
        self.imagepathdisplay.insert(0, "Nenhuma imagem selecionada")
        self.imagepathdisplay.configure(state="readonly")
        self.imagepathdisplay.pack()

        self.imglabel = Label(
            text="Pré visualização", font=("Consolas 10"), pady=5, bg="light gray"
        )
        self.imglabel.pack()

        self.img = ImageTk.PhotoImage(
            PIL.Image.open("defimg.png").resize((490, 450), PIL.Image.ANTIALIAS)
        )
        self.imgpanel = Label(image=self.img)
        self.imgpanel.pack()

        self.startprocess = Button(
            text="Começar",
            command=self.openNewWindow,
            relief=RAISED,
            fg="black",
            bg="light blue",
            borderwidth=1,
            padx=30,
        )
        self.startprocess.pack(side=RIGHT, anchor=SE, pady=5)

        self.closeprocess = Button(
            text="Sair",
            command=root.destroy,
            relief=RAISED,
            fg="black",
            bg="#ed5959",
            borderwidth=1,
            padx=30,
        )
        self.closeprocess.pack(side=LEFT, anchor=SW, pady=5)

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
        img = ImageTk.PhotoImage(img)
        self.imgpanel.configure(image=img)
        self.img = img

    def openNewWindow(self):

        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(self)

        # sets the title of the
        # Toplevel widget
        a = 10 * 2
        newWindow.title("New Window")

        # sets the geometry of toplevel
        newWindow.geometry("200x200")

        # A Label widget to show in toplevel
        Label(newWindow, text=a).pack()
        Label(newWindow, image=self.img).pack()


root = Tk()
root.minsize(720, 700)
root.configure(bg="light gray")
Application(root)
root.mainloop()