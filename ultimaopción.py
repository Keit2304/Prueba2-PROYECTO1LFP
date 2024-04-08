from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import webbrowser
import os


lexemas = []
errores = []

class Lexema:
    def __init__(self, tipo, valor, columna, fila):
        self.tipo = tipo
        self.valor = valor
        self.columna = columna
        self.fila = fila

class Error:
    def __init__(self, mensaje, columna, fila):
        self.mensaje = mensaje
        self.columna = columna
        self.fila = fila
        

def analizadorLexico(textAreaInicial, textAreaFinal, reportArea):
    global lexemas
    global errores

    # Limpiamos las listas de lexemas y errores
    lexemas.clear()
    errores.clear()
    
    caracteres_invalidos = ""
   
    texto = textAreaInicial.get("1.0", "end")
    
    palabra = ""
    fila = 1
    columna = 0
    
    # Obtenemos el texto del text area
    texto = textAreaInicial.get("1.0", "end")
    
    # Iteramos sobre cada caracter del texto
    i = 0
    while i < len(texto):
        char = texto[i]
        columna += 1

        # Verificamos que el caracter sea una letra o un dígito
        if char.isalnum():
            # Iteramos los caracteres para obtener la palabra completa
            while i < len(texto) and texto[i].isalnum():
                palabra += texto[i]
                i += 1

            # Verificar si la palabra es una palabra reservada
            if palabra.lower() in ['doctype', 'html', 'head', 'title', 'body', 'h1', 'p', 'h2']:
                lexemas.append(Lexema("PALABRA_RESERVADA", palabra.lower(), columna, fila))
            elif palabra.isdigit():
                lexemas.append(Lexema("NUMERO", palabra, columna, fila))
            else:
                lexemas.append(Lexema("PALABRA", palabra, columna, fila))
            palabra = ""

        # Verificamos otros caracteres especiales
        elif char in [',']:
            lexemas.append(Lexema("COMA", char, columna, fila))
        elif char in ['.']:
            lexemas.append(Lexema("PUNTO", char, columna, fila))
        elif char in ['+', '-', '*', '/', '<', '>', '!']:
            lexemas.append(Lexema("ESPECIAL", char, columna, fila))
        elif char == '"':  # Verificar si es un inicio de cadena
            cadena = char
            i += 1
            columna += 1
            while i < len(texto) and texto[i] != '"':
                cadena += texto[i]
                i += 1
                columna += 1
            if i < len(texto) and texto[i] == '"':  # Si encontramos el final de la cadena
                cadena += '"'
                lexemas.append(Lexema("CADENA", cadena, columna, fila))
            else:  # Si no encontramos el final de la cadena, hay un error
                errores.append(Error("Cadena sin cerrar", columna, fila))
        # Ignoramos estos caracteres
        elif char in [' ', '\n', '\t', '\r']:
            if char == '\n':
                fila += 1
            columna = 0
        else:
            errores.append(Error(char, columna, fila))

        i += 1
    
    imprimirLexemasYErrores(lexemas, errores, textAreaFinal)
    generarTablaErrores(errores)
    generarTablaLexemas(lexemas)

def generarTablaErrores(errores):
    if errores:
        # Abre el archivo HTML en modo escritura
        with open("tabla_errores.html", "w", encoding="utf-8") as f:
            # Escribe el encabezado del archivo HTML
            f.write("<!DOCTYPE html>\n")
            f.write(f'<html lang="es">\n')
            f.write("<head>\n")
            f.write("<title>Tabla de Errores</title>\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write("<h1>Tabla de Errores</h1>\n")
            
            # Escribe la tabla HTML
            f.write("<table border='1'>\n")
            f.write("<tr><th>Caracter</th><th>Fila</th><th>Columna</th></tr>\n")
            
            # Escribe cada fila de la tabla con la información de los errores
            for error in errores:
                f.write(f"<tr><td>{error.mensaje}</td><td>{error.fila}</td><td>{error.columna}</td></tr>\n")
            
            # Cierra la tabla y el archivo HTML
            f.write("</table>\n")
            f.write("</body>\n")
            f.write("</html>\n")

def generarTablaLexemas(lexemas):
    with open("tabla_lexemas.html", "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n")
        f.write(f'<html lang="es">\n')
        f.write("<head>\n")
        f.write("<title>Tabla de Lexemas</title>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("<h1>Tabla de Lexemas</h1>\n")
        f.write("<table border='1'>\n")
        f.write("<tr><th>Token</th><th>Lexema</th><th>Fila</th><th>Columna</th></tr>\n")
        for lexema in lexemas:
            f.write(f"<tr><td>{lexema.tipo}</td><td>{lexema.valor}</td><td>{lexema.fila}</td><td>{lexema.columna}</td></tr>\n")
        f.write("</table>\n")
        f.write("</body>\n")
        f.write("</html>\n")

def cargarArchivo(textArea):
    archivo = filedialog.askopenfilename(filetypes=[("Archivo de texto", "*.txt, *.html")])

    if archivo:
        with open(archivo, 'r') as f:
            contenido = f.read()

        textArea.delete("1.0", END)
        textArea.insert(END, contenido)

def enviarTexto(textAreaInicial):
    texto = textAreaInicial.get("1.0", "end")
    html_contenido = "<html><head><h1>HTML Traducido</h1></head><body><p>Este es el contenido traducido</p></body></html>"
    return html_contenido

def generarHTML(textAreaInicial, textAreaFinal, reportArea):
    texto = textAreaInicial.get("1.0", "end")
    caracteres_invalidos = analizadorLexico(textAreaInicial, textAreaFinal, reportArea)

    # Verificar si caracteres_invalidos es None
    if caracteres_invalidos is not None:
        for char in caracteres_invalidos:
            texto = texto.replace(char, '')

    return texto


def abrirHTMLGenerado(archivo_entrada):
    # Abrir el archivo de entrada y leer su contenido
    with open(archivo_entrada, 'r') as file:
        lineas = file.readlines()

    # Iniciar el HTML generado
    html_generado = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ejemplo título</title>
    </head>
    <body>
        <div>
    '''

    # Procesar cada línea del archivo para generar el cuerpo del HTML
    for linea in lineas:
        # Eliminar espacios en blanco al inicio y al final de la línea
        linea = linea.strip()
        # Ignorar líneas vacías
        if not linea:
            continue
        # Procesar cada instrucción según su tipo
        if linea.startswith("Inicio"):
            # Si es el inicio, no hacemos nada especial
            continue
        elif linea.startswith("Encabezado"):
            # Agregar el encabezado al HTML generado
            titulo = obtener_valor(linea)
            html_generado += f'<h1>{titulo}</h1>\n'
        elif linea.startswith("Cuerpo"):
            # Abrir un nuevo div para el cuerpo
            html_generado += f'<body>\n'
        elif linea.startswith("Texto"):
            # Agregar texto al HTML generado
            texto = obtener_valor(linea)
            estilo = obtener_valor(linea)
            html_generado += f'<p style="{estilo}">{texto}</p>\n'
        elif linea.startswith("Parrafo"):
            # Agregar párrafo al HTML generado
            texto = obtener_valor(linea)
            estilo = obtener_valor(linea)
            html_generado += f'<h2 style="{estilo}">{texto}</h2>\n'
        elif linea.startswith("Titulo"):
            # Agregar título al HTML generado
            texto = obtener_valor(linea)
            estilo = obtener_valor(linea)
            html_generado += f'<h2 style="{estilo}">{texto}</h2>\n'
        elif linea.startswith("Cursiva"):
            # Agregar texto en cursiva al HTML generado
            texto = obtener_valor(linea)
            estilo = obtener_valor(linea)
            html_generado += f'<div style="{estilo}">{texto}</div>\n'
        elif linea.startswith("Tachado"):
            # Agregar texto tachado al HTML generado
            texto = obtener_valor(linea)
            estilo = obtener_valor(linea)
            html_generado += f'<del style="{estilo}">{texto}</del>\n'
        elif linea.startswith("Subrayado"):
            # Agregar texto subrayado al HTML generado
            texto = obtener_valor(linea)
            estilo = obtener_valor(linea)
            html_generado += f'<div style="{estilo}">{texto}</div>\n'
        elif linea.startswith("Negrita"):
            # Agregar texto en negrita al HTML generado
            texto = obtener_valor(linea)
            estilo = obtener_valor(linea)
            html_generado += f'<div style="{estilo}">{texto}</div>\n'
        elif linea.startswith("Codigo"):
            # Agregar texto con fuente de código al HTML generado
            texto = obtener_valor(linea)
            estilo = obtener_valor(linea)
            html_generado += f'<pre style="{estilo}">{texto}</pre>\n'
        elif linea.startswith("Fondo"):
            # Establecer el color de fondo del HTML generado
            color = obtener_valor(linea)
            html_generado += f'<body style="background-color:{color};">\n'
        else:
            # Si no se reconoce la instrucción, imprimir un mensaje de advertencia
            print("Instrucción no reconocida:", linea)

    # Cerrar el HTML generado
    html_generado += '''
        </div>
    </body>
    </html>
    '''
    # Mostrar el HTML generado
    print(html_generado)

def obtener_valor(linea):
    # Función para obtener el valor de una instrucción
    return linea.split(":")[1].strip().strip(';').strip('"')
# Llamar a la función con el archivo de entrada
archivo_entrada = "entrada.html"
abrirHTMLGenerado(archivo_entrada)

def corregirHTMLGenerado(texto):
    # Separar el texto en bloques de elementos
    bloques = texto.split('},')
    html = "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n\t<meta charset=\"UTF-8\">\n\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n\t<title>Ejemplo título</title>\n</head>\n<body>\n\t<div>\n\t\t<h1>Ejemplo título</h1>\n"

    for bloque in bloques:
        elementos = bloque.split(',')

        for elemento in elementos:
            partes = elemento.split(':')
            etiqueta = partes[0].strip()
            propiedades = partes[1:]

            if etiqueta == "Texto":
                fuente = ""
                color = ""
                tamaño = ""
                estilo = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'fuente':
                        fuente = val.strip().strip('"')
                    elif key.strip() == 'color':
                        color = val.strip().strip('"')
                    elif key.strip() == 'tamaño':
                        tamaño = val.strip().strip('"')
                    elif key.strip() == 'estilo':
                        estilo = val.strip().strip('"')

                html += f"\t\t<div style=\"font-family: {fuente}; color: {color}; font-size: {tamaño}px; font-style: {estilo};\">{propiedades[-1].strip().strip('"}')}</div>\n"

            elif etiqueta == "Cursiva":
                texto = ""
                color = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip().strip('"')
                    elif key.strip() == 'color':
                        color = val.strip().strip('"')

                html += f"\t\t<div style=\"font-style: italic; color: {color};\">{texto}</div>\n"

            elif etiqueta == "Fondo":
                color = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'color':
                        color = val.strip().strip('"')

                html += f"\t\t<div style=\"background-color: {color};\"></div>\n"

            elif etiqueta == "Tachado":
                texto = ""
                color = ""

                for propiedad in propiedades:
                    key, val = propiedad.split(':')
                    if key.strip() == 'texto':
                        texto = val.strip().strip('"')
                    elif key.strip() == 'color':
                        color = val.strip().strip('"')

                html += f"\t\t<div style=\"text-decoration: line-through; color: {color};\">{texto}</div>\n"

    html += "\t</div>\n</body>\n</html>"

    return html

def imprimirLexemasYErrores(lexemas, errores, textArea):
    textArea.delete('1.0', END)
    textArea.insert(END, "Tabla de Lexemas:\n\n")
    for lexema in lexemas:
        textArea.insert(END, f'Tipo: {lexema.tipo}, Valor: {lexema.valor}, Columna: {lexema.columna}, Fila: {lexema.fila}\n')
    textArea.insert(END, "\n\nTabla de Errores:\n\n")
    for error in errores:
        textArea.insert(END, f'Error: {error.mensaje}, Columna: {error.columna}, Fila: {error.fila}\n')

def main():
    root = Tk()
    root.geometry("800x600")
    root.title("Analizador Léxico")

    textAreaInicial = Text(root, height=15, width=100)
    textAreaInicial.pack(pady=20)
    textAreaFinal = Text(root, height=15, width=100)
    textAreaFinal.pack(pady=20)
    reportArea = Text(root, height=10, width=100)
    reportArea.pack(pady=20)
    botonAnalizar = Button(root, text="Analizar", command=lambda: analizadorLexico(textAreaInicial, textAreaFinal, reportArea))
    botonAnalizar.pack(pady=20)
    botonCargar = Button(root, text="Cargar Archivo", command=lambda: cargarArchivo(textAreaInicial))
    botonCargar.pack(pady=20)
    botonGenerar = Button(root, text="Generar HTML", command=lambda: enviarTexto(textAreaInicial))
    botonGenerar.pack(pady=20)
    botonGenerarHTML = Button(root, text="Generar y Abrir HTML", command=lambda: generarHTML(textAreaInicial, textAreaFinal, reportArea))
    botonGenerarHTML.pack(pady=20)
    botonAbrirHTML = Button(root, text="Abrir HTML generado", command=lambda: webbrowser.open('file://' + os.path.realpath('salida.html')))
    botonAbrirHTML.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
