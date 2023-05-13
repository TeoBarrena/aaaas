import PySimpleGUI as sg
import os
import io
from PIL import Image
import editar_perfil as perfil_editar
import configuracion as confi
import collage as coll


#import configuracion as configuracion1 #importo el archivo configuracion
sg.theme ('LightGrey4')

#Se crea esta función para poder abrir las fotos en formatos diferentes al png convirtiendolos en bytes.
def abrir_foto(ruta_foto):
    """
    Se abre la foto desde la ruta (que debe ser pasada por parametro) solo para lectura en formato binario, de esa manera obteniendo los bytes respectivos de la imagen y 
    utilizando el PIL se lee y se la reacomoda en un tamaño de 200x200, guardandandola y enviando a traves del return los bytes de la imagen.
"""
    with open(ruta_foto, 'rb') as file:
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes))
        image.thumbnail((200, 200))
        bio = io.BytesIO()
        image.save(bio, format='PNG')
    return bio.getvalue()


def me (perfil):
    print(perfil)
    ruta_fotos1 = os.path.join(os.getcwd(),"Fotos","signo.png")
    ruta_fotos2 = os.path.join(os.getcwd(),"Fotos","config.png")
    boton_ayuda=[[sg.Button(key ='configuracion', button_color=('LightGrey', 'grey'),image_data=abrir_foto(ruta_fotos2),border_width=0,image_size=(100,100), image_subsample=2),
                 sg.Button(key ='ayuda', button_color=('LightGrey', 'grey'), image_data=abrir_foto(ruta_fotos1),border_width=0,image_size=(100,100),image_subsample=2)]]
    boton_imagen=[[sg.Button(image_data=abrir_foto(perfil['Foto']), image_size=(100,100),image_subsample=2,key='editar_perfil')],
        [sg.Text((f"-{perfil['Alias']}-"),justification='center', size=(10, 1), font=('Helvetica', 12), border_width=2, text_color='black')]]

    barra_principal = [[sg.Column(boton_imagen, element_justification='left', expand_x=True),
                        sg.Column(boton_ayuda, element_justification='rigth', expand_x=True)]]

    
    #ruta_foto = os.path.join(os.getcwd(),"Fotos","ayuda.png")

    layout = [[barra_principal],
        [sg.Button("Etiquetar Imagenes", size=(40, 4), button_color=('Black', 'mediumpurple'), font=('Helvetica', 17), border_width=2)], #mediumorchid
        [sg.Button("Generar Meme", size=(40, 4), button_color=('Black', 'LightBlue'), font=('Helvetica', 17), border_width=2)],
        [sg.Button("Generar Collage", size=(40, 4), button_color=('Black', 'skyblue'), font=('Helvetica', 17), border_width=2)],
        [sg.Button("Salir", size=(40, 4), button_color=('Black', 'steelblue'), font=('Helvetica', 17), border_width=2)]
    ]

    
    foto_ayuda = os.path.join(os.getcwd(),"Fotos","ayudaa.png")
    window = sg.Window('',layout, element_justification='c', size=(1366,768))
    while True:
        event, values = window.read()
        if ((event == sg.WIN_CLOSED) or (event == "Salir")):
            break
        if event =="Generar Collage":
            coll.coll()
        if event == 'configuracion': #solo puedo acceder una vez a configuracion, despues se rompe
            window.hide()
            confi.conf(perfil["Alias"])
            window.UnHide()
        if event == "ayuda":
            sg.popup(image=abrir_foto(foto_ayuda))
        if event == 'editar_perfil':
            perfil = perfil_editar.editar_perfil(perfil)
            window['editar_perfil'].update(image_data=abrir_foto(perfil['Foto']), image_size=(100,100),image_subsample=2)
                #sg.Popup(configuracion1.conf()) #con este se puede seguir accediendo a configuracion pero solo deja guardar la primera vez
    window.close()