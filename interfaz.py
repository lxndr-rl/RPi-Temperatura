from tkinter import *
import json
from tkinter import ttk, filedialog
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from os import listdir
from os.path import isfile, join
import random
import RPi.GPIO as GPIO
import dht11
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("PIS")
        self.minsize(590, 400)

        self.labelFrame = ttk.LabelFrame(self, text="Sensar Temperatura")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)
        
        img = Image.open('./imagenes/no_Fruta.jpg')
        img = img.resize((450, 350), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.label2 = Label(image=photo)
        self.label2.image = photo
        self.label2.grid(column=2, row=4)
        estado = Image.open('./imagenes/nada.png')
        estado = estado.resize((30, 30), Image.ANTIALIAS)
        photoEstado = ImageTk.PhotoImage(estado)
        self.label3 = Label(self.labelFrame, image=photoEstado)
        self.label3.image = photoEstado
        self.label3.grid(column=1, row=30)
        self.button()

    def button(self):
        self.n = tk.StringVar()
        self.product = ttk.Combobox(self.labelFrame, width=27, textvariable=self.n)
        self.product['values']=('Naranja','Cacao')
        self.product.current(0)
        self.button = ttk.Button(self.labelFrame, text="Empezar", command=self.sensar)
        self.product.grid(column=1, row=1)
        self.button.grid(column=3, row=4)
        self.temperatura = ttk.Label(self.labelFrame, text="")
        self.temperatura.grid(column=1, row=6)
        self.problemas = ttk.Label(self.labelFrame, text="")
        self.problemas.grid(column=1, row=10)
        self.humedad = ttk.Label(self.labelFrame, text="")
        self.humedad.grid(column=1, row=14)
        self.suelo = ttk.Label(self.labelFrame, text="")
        self.suelo.grid(column=1, row=18)
        self.ph = ttk.Label(self.labelFrame, text="")
        self.ph.grid(column=1, row=22)
        self.agua = ttk.Label(self.labelFrame, text="")
        self.agua.grid(column=1, row=26)
    
    def sensar(self):
        def randImg(tipo):
            imagenesCacao = [f for f in listdir(f'./imagenes/{tipo}') if isfile(join(f'./imagenes/{tipo}', f))]
            return f'./imagenes/{tipo}/{imagenesCacao[random.randint(0,len(imagenesCacao)-1)]}'
        cont = 1
        acum = 0
        with open('recomendaciones.json') as recom_file: 
            recomendaciones = json.load(recom_file) 
        recom_file.close()
        try:
            img = Image.open(randImg(self.n.get()))
            img = img.resize((450, 350), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)

            estado = Image.open('./imagenes/loading.png')
            estado = estado.resize((30, 30), Image.ANTIALIAS)
            photoEstado = ImageTk.PhotoImage(estado)
        except:
            return
        self.label2 = Label(image=photo)
        self.label2.image = photo
        self.label2.grid(column=2, row=4)
        
        self.label3 = Label(self.labelFrame, image=photoEstado)
        self.label3.image = photoEstado
        self.label3.grid(column=1, row=30)

        self.temperatura.configure(text=f"Temperatura: {recomendaciones[self.n.get()]['temperatura']}")
        
        self.problemas.configure(text=f"Complicaciones: {recomendaciones[self.n.get()]['problemas']}")

        self.humedad.configure(text=f"Humedad: {recomendaciones[self.n.get()]['humedad']}")
        
        self.suelo.configure(text=f"Tipo de Suelo: {recomendaciones[self.n.get()]['suelo']}")
        
        self.ph.configure(text=f"PH: {recomendaciones[self.n.get()]['ph']}")

        self.agua.configure(text=f"Agua: {recomendaciones[self.n.get()]['agua']}")

        while cont<=10:
            instance = dht11.DHT11(pin = 14)
            result = instance.read()
            if result.is_valid():
                acum += result.temperature
                cont += 1
            else:
                print(f"Error: {result}")
            time.sleep(2)
        temp = acum/cont

        if(temp>recomendaciones[self.n.get()]['tempMin'] and temp<recomendaciones[self.n.get()]['tempMax']):
            estado = Image.open('./imagenes/ok.png')
            estado = estado.resize((30, 30), Image.ANTIALIAS)
            photoEstado = ImageTk.PhotoImage(estado)
            self.label3 = Label(self.labelFrame, image=photoEstado)
            self.label3.image = photoEstado
            self.label3.grid(column=1, row=30)
            messagebox.showinfo('Resultados', f'La temperatura es perfecta: {temp}')
        elif (temp<recomendaciones[self.n.get()]['tempMin']):
            estado = Image.open('./imagenes/alert.png')
            estado = estado.resize((30, 30), Image.ANTIALIAS)
            photoEstado = ImageTk.PhotoImage(estado)
            self.label3 = Label(self.labelFrame, image=photoEstado)
            self.label3.image = photoEstado
            self.label3.grid(column=1, row=30)
            messagebox.showwarning('Resultados', f'La temperatura está por debajo del mínimo: {temp}')
        else:
            estado = Image.open('./imagenes/alert.png')
            estado = estado.resize((30, 30), Image.ANTIALIAS)
            photoEstado = ImageTk.PhotoImage(estado)
            self.label3 = Label(self.labelFrame, image=photoEstado)
            self.label3.image = photoEstado
            self.label3.grid(column=1, row=30)
            messagebox.showwarning('Resultados', f'La temperatura está por encima del máximo: {temp}')

        

root = Root()
root.mainloop()
