from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import webbrowser
import os

class Lexema:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class Error:
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
def analizadorLexico(textAreaInicial, textAreaFinal, reportArea):
    lexemas = []
    errores = []
    caracteres_invalidos = ""
    palabra = ""
   
    texto = textAreaInicial.get("1.0", "end")
    
    i = 0
    while i < len(texto):
        char = texto[i]

        if char.isalnum():
            while i < len(texto) and texto[i].isalnum():
                palabra += texto[i]
                i += 1

            if palabra.lower() in ['doctype', 'html', 'head', 'title', 'body', 'h1', 'p', 'h2']:
                lexemas.append(Lexema("PALABRA_RESERVADA", palabra.lower()))
            elif palabra.isdigit():
                lexemas.append(Lexema("NUMERO", palabra))
            else:
                lexemas.append(Lexema("PALABRA", palabra))
            palabra = ""

        elif char in [',']:
            lexemas.append(Lexema("COMA", char))
        elif char in ['.']:
            lexemas.append(Lexema("PUNTO", char))
        elif char in ['+', '-', '*', '/', '<', '>', '!']:
            lexemas.append(Lexema("ESPECIAL", char))
        elif char in [' ', '\n', '\t', '\r']:
            pass
        else:
            errores.append(Error(f"Caracter no válido: {char}"))
            caracteres_invalidos += char

        i += 1
    
    imprimirLexemasYErrores(lexemas, errores, textAreaFinal)
    reportArea.delete("1.0", END)
    reportArea.insert(END, caracteres_invalidos)

def cargarArchivo(textArea):
    archivo = filedialog.askopenfilename(filetypes=[("Archivo de texto", "*.txt, *.html")])

    if archivo:
        with open(archivo, 'r') as f:
            contenido = f.read()

        textArea.delete("1.0", END)
        textArea.insert(END, contenido)

def enviarTexto(textAreaInicial):
    texto = textAreaInicial.get("1.0", "end")
    # Aquí deberías enviar el texto al servidor y obtener el código HTML traducido
    # Supongamos que la variable html_contenido contiene el código HTML traducido
    html_contenido = "<html><head><title>HTML Traducido</title></head><body><p>Este es el contenido traducido</p></body></html>"
    return html_contenido

def generarHTML(textAreaInicial):
    texto = textAreaInicial.get("1.0", "end")
    caracteres_invalidos = analizadorLexico(texto)
    # Reemplazar los caracteres no válidos en el texto original
    for char in caracteres_invalidos:
        texto = texto.replace(char, '')
    return texto

def abrirHTMLGenerado(textAreaInicial, textAreaFinal):
    texto = textAreaInicial.get("1.0", "end")
    # Corregir el HTML generado
    html_corregido = corregirHTMLGenerado(texto)
    # Mostrar el HTML corregido en el textAreaFinal
    textAreaFinal.delete("1.0", END)
    textAreaFinal.insert(END, html_corregido)

def generar_estilo(propiedad, valor):
    if propiedad == "fuente":
        return f"font-family: {valor}; "
    elif propiedad == "color":
        return f"color: {valor}; "
    elif propiedad == "tamaño":
        return f"font-size: {valor}px; "
    elif propiedad == "estilo":
        if valor == "negrita":
            return "font-weight: bold; "
        elif valor == "cursiva":
            return "font-style: italic; "
    elif propiedad == "posicion":
        if valor == "centro":
            return "text-align: center; "
        elif valor == "izquierda":
            return "text-align: left; "
        elif valor == "derecha":
            return "text-align: right; "
    elif propiedad == "fondo":
        return f"background-color: {valor}; "
    elif propiedad == "del":
        return f"text-decoration: line-through; color: {valor}; "
    elif propiedad == "subrayado":
        return f"text-decoration: underline; color: {valor}; "
    return ""


def corregirHTMLGenerado(texto):
    # Separar el texto en bloques de elementos
    bloques = texto.split('},')

    html = "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n\t<meta charset=\"UTF-8\">\n\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t<title>Ejemplo título</title>\n</head>\n<body>\n\t<div>\n\t\t<h1>Ejemplo título</h1>\n"

    for bloque in bloques:
        elementos = bloque.split(',')

        etiqueta = elementos[0].split(':')[-1].strip().capitalize()

        html += f"\t\t<{etiqueta} style=\""

        for elemento in elementos[1:]:
            partes = elemento.split(':')
            propiedad = partes[0].strip()
            valor = partes[1].strip().strip('"')

            if propiedad == "texto":
                html += f">{valor}</{etiqueta}>\n"
            else:
                html += generar_estilo(propiedad, valor)

        html += "\t\t</div>\n"

    html += "</body>\n</html>"
    
    return html


texto = '''Inicio:{
    Encabezado:{
        TituloPagina:"Ejemplo titulo";
    },
    Cuerpo:[
        Texto:{
            fuente:"Arial";
            color:"azul";
            tamaño:"11";
            estilo:"normal";
        },
        Cursiva:{
            texto:"Este es un texto en cursiva.";
            color:"azul";
        },
        Fondo:{
            color:"#FFA07A";
        },
        Tachado:{
            texto:"Este es un texto tachado.";
            color:"rojo";
        }
    ]
}'''

html_corregido = corregirHTMLGenerado(texto)
print(html_corregido)


def Traductor():
    root = Tk()
    root.title("Traductor")
    root.geometry("800x600")
    frm = ttk.Frame(root)
    frm.pack(fill=BOTH, expand=True)

    labelInput = ttk.Label(frm, text="Texto de entrada")
    labelInput.grid(row=0, column=0, padx=10, pady=5)

    textAreaInicial = Text(frm, width=50, height=25)
    textAreaInicial.grid(row=1, column=0, padx=10, pady=10)

    labelOutput = ttk.Label(frm, text="Traducción")
    labelOutput.grid(row=0, column=1, padx=10, pady=5)

    textAreaFinal = Text(frm, width=50, height=25)
    textAreaFinal.grid(row=1, column=1, padx=10, pady=10)

    reportLabel = ttk.Label(frm, text="Caracteres no válidos:")
    reportLabel.grid(row=2, column=0, padx=10, pady=5)

    reportArea = Text(frm, width=50, height=5)
    reportArea.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    buttonFrame = ttk.Frame(frm)
    buttonFrame.grid(row=4, column=0, columnspan=2, pady=10)

    ttk.Button(buttonFrame, text="Abrir Archivo", command=lambda: cargarArchivo(textAreaInicial)).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(buttonFrame, text="Traducir", command=lambda: analizadorLexico(textAreaInicial, textAreaFinal, reportArea)).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(buttonFrame, text="Abrir HTML Generado", command=lambda: abrirHTMLGenerado(textAreaInicial, textAreaFinal)).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(buttonFrame, text="Regresar", command=root.destroy).grid(row=0, column=3, padx=5, pady=5)

    root.mainloop()

def imprimirLexemasYErrores(lexemas, errores, textAreaFinal):
    textAreaFinal.delete("1.0", END)
    textAreaFinal.insert(END, "-----------------------------------\n")
    textAreaFinal.insert(END, "Lexemas:\n")
    for lexema in lexemas:
        textAreaFinal.insert(END, f"{lexema.tipo}: {lexema.valor}\n")

    textAreaFinal.insert(END, "-----------------------------------\n")
    textAreaFinal.insert(END, "Errores:\n")
    for error in errores:
        textAreaFinal.insert(END, f"{error.mensaje}\n")


def main():
    root = Tk()
    root.title("Menú Principal")
    root.geometry("300x300")
    frm = ttk.Frame(root)
    frm.pack(fill=BOTH, expand=True)
    ttk.Label(frm, text="Nombre: Keitlyn Valentina Tunchez Castañeda").pack(pady=5)
    ttk.Label(frm, text="Carnet: 202201139").pack(pady=5)
    ttk.Label(frm, text="Curso: Lenguajes Formales y de Programación").pack(pady=5)

    buttonFrame = ttk.Frame(frm)
    buttonFrame.pack(pady=90)

    ttk.Button(buttonFrame, text="Abrir Traductor HTML", command=Traductor).pack(side=LEFT, padx=5)
    ttk.Button(buttonFrame, text="Salir", command=root.destroy).pack(side=LEFT, padx=5)

    root.mainloop()

main()