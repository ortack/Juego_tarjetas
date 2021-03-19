from tkinter import *
from tkinter import messagebox
import pandas
import random
import pyttsx3
import os


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
try:
    data = pandas.read_csv('data/words_to_learn.csv') #intenta cargar el fichero de las palabrs que nos faltan
except FileNotFoundError: # si no existe cargamos el original
        original_data = pandas.read_csv('data/french_words.csv')
        to_learn = original_data.to_dict(orient='records')

else:
    to_learn = data.to_dict(orient='records')  # convietes los datos a un diccionario pero dara value es un key


def next_card(): # funcion para cargar una nueva palabra
    global current_card, flip_timer
    window.after_cancel(flip_timer) #paramos el relog
    current_card = random.choice(to_learn) # selecionamos aleatoriamente la palabra del diccionario
    idioma_origen = list(current_card.keys())[0] #sacamso el nombre del idioma de origen
    canvas.itemconfig(card_title, text=idioma_origen, fill='black') # lo pintamos en la tarjeta
    canvas.itemconfig(card_word, text=current_card[idioma_origen], fill='black') # pintamos la palabra
    canvas.itemconfig(card_backgrond, image=card_img_front) # cambiamos el fondo al frente
    engine = pyttsx3.init() # instancia de la ingenieria de voz
    engine.setProperty('rate', 125) # cambiamso la velocidad de habla
    engine.say(current_card[idioma_origen]) # le decimos la pablara
    engine.runAndWait() # lo ponemos



    LLLL




    
    flip_timer = window.after(3000, func=flip_card) # volvemos a arrancar el relog

def is_known(): # funcion para cuando sabemos una palabra
    global current_card, to_learn
    to_learn.remove(current_card) # borramos la palabra del diccionario
    data = pandas.DataFrame(to_learn) # convertimos el diccionario en un dataframe
    data.to_csv('data/words_to_learn.csv', index=False) # salvamos a csv sin los indexes
    next_card() # llamaos a la siguente palabra


def flip_card(): # funcion para cambiar a ver la respuesta
    idioma_destino = list(current_card.keys())[1] # sacamos el nombre del imdioma de destino
    canvas.itemconfig(card_title, text=idioma_destino, fill='white') # lo pintamos en la tarjeta
    canvas.itemconfig(card_word, text=current_card[idioma_destino], fill='white') # pintamos la palabra
    canvas.itemconfig(card_backgrond, image =card_img_back)# cambiamos el fondo a de atras
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)
    engine.say(current_card[idioma_destino])
    engine.runAndWait()



window = Tk()  # creo la ventana
window.title('Juego de Palabras')  # le doy un titulo
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)  # la configuro

flip_timer = window.after(3000, func=flip_card) # arrancamos relog en una varible para usarlo despues

canvas = Canvas(width=800, height=525, bg=BACKGROUND_COLOR, highlightthickness=0) # creamos el canvas de imagen
card_img_front = PhotoImage(file='images/card_front.png') # cargamos la imgagen del frente
card_img_back = PhotoImage(file='images/card_back.png') # cargamos la imagen del fondo
card_backgrond = canvas.create_image(400, 262, image=card_img_front) # ponemos la del frente
card_title = canvas.create_text(400, 150, text='', font=('Arial', 40, 'italic')) # le añadimos el texto del titulo
card_word = canvas.create_text(400, 262, text='', font=('Arial', 60, 'bold')) # le añadimos el texto de la palabra
canvas.grid(column=0, row=0, columnspan=2) # la posicinamos en la ventana


right_image = PhotoImage(file="images/right.png") # cargamos la imagen para el boton
right_button = Button(image=right_image, highlightthickness=0, command=is_known) # creamos el boton de right
right_button.grid(column=1, row=1) # lo posicionamos el la ventana

wrong_image = PhotoImage(file="images/wrong.png") # cargamos la imagen para el boton de wrong
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card) # creamos el boton de worgh
wrong_button.grid(column=0, row=1) # lo poscionamos el la ventana


next_card() # llemamos para la primera palabra

window.mainloop() # loop  de la ventana