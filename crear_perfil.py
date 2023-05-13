import PySimpleGUI as sg
import os,io
import json
from PIL import Image
import datetime
import csv
datos =[]


def agregar_perfil():
    hora = datetime.datetime.now().time()
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    global datos
    #imagen predeterminada
    ruta_imagen = os.path.join(os.getcwd(),"Fotos","usuario.png")
    
    #si el archivo esta vacio da error el json.load
    if os.path.getsize('perfiles.json') > 0:
        with open('perfiles.json') as archivo:
            datos = json.load(archivo)

    #layout
    layout = [[sg.Text('Nuevo Perfil',font=('Helvetica',15)),sg.Button("< Volver", button_color=('black', 'white'),border_width=0,pad=(250,10))],
          [sg.Text('Nick o alias',font=('Helvetica',10))],
          [sg.InputText()],
          [sg.Text('Nombre',font=('Helvetica',10))],
          [sg.InputText()],
          [sg.Text('Edad',font=('Helvetica',10))],
          [sg.Input()],
          [sg.Text('Genero autopercibido',font=('Helvetica',10))],
          [sg.Combo(['Masculino','Femenino','Otro'],default_value='Selecciona una opcion',key='Genero',size=(30,1),readonly=True)], #combo es una lista desplegable
          [sg.Image(ruta_imagen, key='-AVATAR_IMAGE-')],
          [sg.Button("Seleccionar avatar",key='-AVATAR-')],
          [sg.Button('Guardar',pad=(400,10),size=(8,2),button_color=('sky blue'))]]
    window= sg.Window("Crear nuevo perfil",layout,size=(1366,768))
    
    while True:
        event,values = window.read()

        #cambio de imagen de usuario
        if event == '-AVATAR-':
            ruta_imagen = sg.popup_get_file('Seleccionar avatar', no_window=True, file_types=(('Imagenes', '*.png *.jpg *.jpeg *.gif *.bmp *.tiff'),))
            if ruta_imagen:
                try:
                    #if(ruta_imagen == ""):
                        #ruta_imagen = os.path.join(os.getcwd(),"Fotos","usuario.png")
                    #else:
                    with open(ruta_imagen, 'rb') as file:
                        img_bytes = file.read()
                        image = Image.open(io.BytesIO(img_bytes))
                        image.thumbnail((150, 150))
                        bio = io.BytesIO()
                        image.save(bio, format='PNG')
                        window['-AVATAR_IMAGE-'].update(data=bio.getvalue())
                except Exception as e:
                    sg.popup_error(f'Error al cargar la imagen: {e}')
            else: #si entras a cambiar foto y volves sin elegir foto sigue con la predeterminada
                ruta_imagen = os.path.join(os.getcwd(),"Fotos","usuario.png")

        #cerrado
        if event=="CANCELAR" or event== sg.WINDOW_CLOSED or event == "< Volver":
            break

        #guardado del perfil
        if event=='Guardar':

            #verificacion campos completos
            if any(len(values[key]) == 0 for key in values) or values['Genero'] == 'Selecciona una opcion':
                sg.popup('Por favor complete todos los campos.')
                continue
            alias = values[0]
            nombre=values[1]

            #verificacion edad sea un entero
            while True:
                try:
                    edad = int(values[2])
                    break
                except ValueError:
                    sg.popup('Por favor ingrese un número entero válido para la edad.')
                    event, values = window.read()#se declara de vuelta para que lea el nuevo valor de edad ingresado
                    continue
            foto = ruta_imagen

            #como guardar el genero
            if values['Genero'] == 'Otro':
                genero = sg.popup_get_text("Complete manualmente su genero")
            else:
                genero = values['Genero']

            #guardado de datos
            datos.append({"Nombre": nombre,"Edad": edad,"Alias":alias,"Genero":genero,"Foto":foto})

            #verificar alias unico
            alias_existente = [d["Alias"] for d in datos[:-1]] #agarra del primero hasta el anteultimo, el ultimo lo excluye
            if alias in alias_existente:
                while True:
                   nuevo_alias = sg.popup_get_text("Ese alias ya existe, ingrese otro")
                   if nuevo_alias is None or nuevo_alias == '': #en caso de apretar cancel se ejecuta el while de nuevo, para asegurar que elije algun alias que no se repite
                        continue
                   elif nuevo_alias == alias:
                       continue
                   elif nuevo_alias in alias_existente: #la segunda condicion se toma por si apretan el boton cancelar
                        continue #vuelve a entrar al while
                   else:
                        datos[-1]['Alias'] = nuevo_alias
                        break
            #agregar al archivo JSON
            with open('perfiles.json','w') as archivo:
                json.dump(datos,archivo,indent= 2)
                archivo.write('\n') # se agrega un salto de línea para escribir la siguiente lista en la siguiente línea         
            #agregar nueva operacion al archivo CSV
            with open ('perfiles.csv','a',newline='') as archivo:
                writer = csv.writer(archivo)
                writer.writerow([fecha,hora,datos[-1]["Alias"],"Creo perfil"]) 
            sg.popup('Perfil creado con éxito')
            break
    window.close()
    if datos!= []:
        return datos[-1]