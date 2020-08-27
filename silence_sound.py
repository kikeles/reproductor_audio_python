from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import pygame
import os 
from mutagen.mp3 import MP3
import time
import threading
#inicializar el mixer y funciones del pygame
pygame.init()
ruta = "lista.txt" #nombre del archivo
pausado = False
playing = False
#funciones de reproduccion
def play(track):
	global pausado
	global playing

	if pausado:
		pygame.mixer.music.unpause()#no pausado en caso de no haber presionado pause y el audio continua reproduciendose
		pausado = False
		barra_estado['text'] = play_duracion
	else:
		try:	
		    pygame.mixer.music.load(track)#solo archivos (mp3)
		    pygame.mixer.music.play()
		    barra_estado['text'] = "Play "+track
		except:
			tkinter.messagebox.showinfo("ERROR","ARCHIVO MP3 NO ENCONTRADO")
			nombre_audio = ""
			duracion=""
		else:
			playing = True
			tiempo_duracion()


def stop():
	pygame.mixer.music.stop()
	barra_estado['text'] = "STOP - " + nombre_audio

#pausado = False
def pause():
	global pausado
	pausado = True
	pygame.mixer.music.pause()
	barra_estado['text'] = "PAUSE - " + nombre_audio


def volumen(valor):
	escala = int(valor) / 100
	pygame.mixer.music.set_volume(escala)


def tiempo_duracion():
	global duracion
	global play_duracion
	archivo_audio = MP3(nombre_audio)
	tiempo_total = archivo_audio.info.length
	minutos,segundos = divmod(tiempo_total,60) #648768768.6548384384
	minutos = round(minutos)
	segundos = round(segundos)
	duracion = "{:02d}:{:02d}".format(minutos,segundos)#verificar el format para poner minutos y segundos
	play_duracion = "PLAY - " + nombre_audio + "        Duración - "+duracion
	barra_estado['text'] = play_duracion
	
	thread1 = threading.Thread(target=tiempo_reproduccion,args=(tiempo_total,))
	thread1.start()

def tiempo_reproduccion(tiempo):
	global pausado #si se presiona pause no entra en el thread y continua el conteo
	#pygame.mixer.music.get_busy() esta funcion retorna False cuando es presionado el boton stop 
	x = 0
	while x<=tiempo and pygame.mixer.music.get_busy():
		if pausado:#si se presiono pause entra
			continue
		else:
			minutos,segundos = divmod(x,60)
			minutos = round(minutos)
			segundos = round(segundos)
			formato_t = "{:02d}:{:02d}".format(minutos,segundos)
			labelTiempo['text'] = "Reproducción    [ "+formato_t+" ]"
			print(formato_t)
			time.sleep(1)
			x += 1


#extraer nombre del archivo
def cargar_archivo_mp3():
	global nombre_audio
	formato = ".mp3"
	nombre = extraer_nombre_mp3() #trackNombre.get()
	nombre_audio = nombre+formato
	if nombre == "":
		tkinter.messagebox.showinfo("Información","Es probable que no exista el archivo en la lista")
		barra_estado['text'] = "ARCHIVO no definido en la lista..."
	else:
		play(nombre_audio)

#extraer el contenido del item seleccionado
def extraer_nombre_mp3():
	fila = ""
	indice_item = lista_reproduccion.curselection()
	for item in indice_item:
		fila = lista_reproduccion.get(item)
	lista = fila.split("----")
	titulo = lista[0]
	elemento1 = titulo.split(":")
	if fila == "":
		tkinter.messagebox.showinfo("Información","Selecciona el nombre de tu archivo mp3 en tu lista")
		stop()
		barra_estado['text'] = "ARCHIVO no definido en la lista..."
		return fila
	else:
		#metodo strip() retorna una copia de una cadena con ciertos caracteres eliminados de su principio y final
		nombre_mp3 = elemento1[1].strip(" ")
		print("nombre_mp3:"+nombre_mp3)
		return nombre_mp3

#manejo de archivos
def guardar():
	cadena = "Titulo: "+txt_titulo.get()+"/Genero: "+ txt_genero.get()+"/Artista: "+ txt_artista.get()
	with open(ruta, mode="a", encoding="utf-8") as fichero:
		fichero.write(cadena+"\n")
	fichero.close()
	barra_estado['text'] = "Guardar en la lista  ..." + cadena
	txt_titulo.set("")
	txt_genero.set("")
	txt_artista.set("")

def eliminar():
	indice_item = lista_reproduccion.curselection()
	for item in indice_item:
		fila = lista_reproduccion.get(item)
		lista_reproduccion.delete(item)
	
	if playing == True:
		stop()
	barra_estado['text'] = "Eliminar de la lista  ..." +fila 
	
	nuevofichero = open("nuevaLista.txt", mode="a",encoding="utf-8")
	lista = fila.split("----")
	item_seleccionado = lista[0]+"/"+lista[1]+"/"+lista[2]
	with open(ruta, mode="r") as fichero:
			i = 0
			cadena = fichero.readline()
			while cadena != "":
				if cadena == item_seleccionado:
					pass
				else:
					nuevofichero.write(cadena)
				i += 1
				cadena = fichero.readline()
			nuevofichero.close()
			fichero.close()
	
	#eliminar lista
	os.remove("lista.txt")
	#renombrar lista
	os.rename("nuevaLista.txt","lista.txt")



def mostrar():
	try:
		barra_estado['text'] = "Mostrar elementos de la lista"
		lista_reproduccion.delete(0,END)
		with open(ruta, mode="r") as fichero:
			i = 0
			cadena = fichero.readline()
			while cadena != "":
				lista = cadena.split("/")
				lista_reproduccion.insert(i, lista[0]+"----"+lista[1]+"----"+lista[2])
				i += 1
				cadena = fichero.readline()
			fichero.close()
	except FileNotFoundError:
		tkinter.messagebox.showerror("ERROR","No existen elementos en la lista")
	

#inicio de ventana principal
v_principal = Tk()
txt_titulo = StringVar()
txt_genero = StringVar()
txt_artista = StringVar()
colorPlay = "#EE9307"
colorLetra = "#FFF"
colorDatos = "#006"
colorLista = "#FF3950"
v_principal.geometry("500x500")
v_principal.title("Silence Sound")
v_principal.config(bg="#355A92")



"""
SECCION LABELS
"""
#datos del audio
labelTitulo = Label(v_principal,text="Título",bg=colorDatos,fg=colorLetra,font=("Arial",10)).place(x=65,y=10)
labelGenero = Label(v_principal,text="Género",bg=colorDatos,fg=colorLetra,font=("Arial",10)).place(x=230,y=10)
labelArtista = Label(v_principal,text="Artista",bg=colorDatos,fg=colorLetra,font=("Arial",10)).place(x=390,y=10)

#label volumen
labelVolumen = Label(v_principal,text="Volumen",bg="#355A92",fg=colorLetra,font=("Arial",10)).place(x=218,y=460)

#tiempo de ejecucion del audio
frame_reproduccion = Frame(v_principal)
frame_reproduccion.place(x=183,y=312)
labelTiempo = Label(frame_reproduccion,text="Reproducción    [ 00:00 ]",anchor=W,fg=colorLetra,bg="#2A2D32",relief=GROOVE)
labelTiempo.pack()

#barra de estado
barra_estado = Label(v_principal,text="Iniciando Silence Sound",relief=SUNKEN, anchor=W, bg="#8CDFFB")
barra_estado.pack(side=BOTTOM, fill=X)



"""
SECCION ENTRADA DE DATOS
"""
#entrada de datos
trackTitulo = Entry(v_principal,textvariable=txt_titulo,font=("Arial",10)).place(x=15,y=35)
trackGenero = Entry(v_principal,textvariable=txt_genero,font=("Arial",10)).place(x=180,y=35)
trackArtista = Entry(v_principal,textvariable=txt_artista,font=("Arial",10)).place(x=340,y=35)


"""
Frame listbox
creando el frame del listbox
"""
frame = Frame(v_principal,relief=SUNKEN)
frame.place(x=100,y=100)
lista_reproduccion = Listbox(frame ,height=9,width=50)
lista_reproduccion.insert(0,"Título:              Género:              Artista:")#20 espacios
#lista_reproduccion.pack(side="left", fill="y")
lista_reproduccion.grid(row=0, column=0,sticky=N+S+E+W)


#scrollbars del listbox
scrollbarY = Scrollbar(frame, orient="vertical")
scrollbarY.config(command=lista_reproduccion.yview)
#scrollbarY.pack(side="right")
scrollbarY.grid(row=0, column=1, sticky=N+S)

scrollbarX = Scrollbar(frame, orient="horizontal")
scrollbarX.config(command=lista_reproduccion.xview)
#scrollbarX.pack(side="bottom")
scrollbarX.grid(row=1, column=0, sticky=E+W)


lista_reproduccion.config(yscrollcommand=scrollbarY.set)
lista_reproduccion.config(xscrollcommand=scrollbarX.set)


"""
SECCION BOTONES
"""
#guardar en la lista
btn_guardar = Button(v_principal,text="Guardar",command=guardar,bg=colorLista,fg=colorLetra).place(x=145,y=65)
#eliminar de la lista
btn_eliminar = Button(v_principal,text="Eliminar",command=eliminar,bg=colorLista,fg=colorLetra).place(x=305,y=65)
#mostrar elementos de la lista
btn_mostrar = Button(v_principal,text="Mostrar Lista",command=mostrar,bg=colorLista,fg=colorLetra).place(x=210,y=275)

#boton parar 
imgStop = PhotoImage(file="imagen/stop50x50.png")
btn_stop = Button(v_principal,image=imgStop,command=stop,bg=colorPlay).place(x=120,y=350)

#boton reproducir
imgPlay = PhotoImage(file="imagen/play50x50.png")
btn_play = Button(v_principal,image=imgPlay,command=cargar_archivo_mp3,bg=colorPlay).place(x=220,y=350)

#boton pausar
imgPause = PhotoImage(file="imagen/pause50x50.png")
btn_play = Button(v_principal,image=imgPause,command=pause,bg=colorPlay).place(x=320,y=350)

#barra de volumen
btn_volumen = Scale(v_principal, from_=0, to=100, orient=HORIZONTAL, bg=colorPlay,fg=colorLetra,command=volumen)
btn_volumen.set(100)
btn_volumen.place(x=195,y=420)

#ejecucion de la interfaz
v_principal.mainloop()
