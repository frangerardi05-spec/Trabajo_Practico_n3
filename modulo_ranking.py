#---------#     Módulo que contiene el código para Mostrar los Rankings del TP_3 de Programación I   #---------#

# Ruta RELATIVA del archivo donde se guarda el ranking (formato CSV)
RUTA_RANKING = "ranking.csv"

#--------------------------------------------------------#
# Funciones para el archivo
def pedir_nombre_jugador()->str:
    """
    Función que le pide al usuario su nombre y lo valida:
        - No puede estar vacío.
        - No puede tener comas (porque la coma es el separador del CSV).
    Lo devuelve con .capitalize() para que "pepe", "PEPE" y "Pepe" sean el mismo jugador.

    Retorna el nombre validado (str).
    """
    nombre = input("> Ingresá tu nombre de jugador: ").strip()
    while nombre == "" or buscar_caracter(nombre, ",") == True:
        print("Nombre inválido. No puede estar vacío ni tener comas.")
        nombre = input("> Ingresá tu nombre de jugador: ").strip()
    return nombre.capitalize()

def buscar_caracter(cadena:str, caracter:str)->bool:
    """
    Función que busca un carácter dentro de una cadena.

    Recibe como parámetros:
        cadena (str)   |   caracter (str)

    Retorna True si lo encuentra, False si no.
    """
    retorno = False
    for letra in cadena:
        if letra == caracter:
            retorno = True
            break
    return retorno

def leer_archivo_csv(ruta:str)->str|None:
    """
    Función que abre el archivo en modo lectura ("r") y retorna todo su contenido como string.
    Si el archivo no existe, open() tira error, por eso se usa try/except.

    Recibe como parámetro:
        ruta (str)

    Retorna el contenido (str) o None si el archivo no existe.
    """
    try:
        with open(ruta, "r") as archivo:
            datos = archivo.read()
    except:
        datos = None
    return datos

def escribir_archivo(texto:str, ruta:str)->None:
    """
    Función que abre el archivo en modo escritura ("w") y escribe el texto.
    CUIDADO: el modo "w" BORRA todo lo que había antes. Solo se usa para crear
    el archivo por primera vez con el encabezado.

    Recibe como parámetros:
        texto (str)   |   ruta (str)
    """
    with open(ruta, "w") as archivo:
        archivo.write(texto)

def anexar_linea(linea:str, ruta:str)->None:
    """
    Función que abre el archivo en modo anexado ("a") y agrega una línea al final,
    SIN borrar los registros anteriores.

    Recibe como parámetros:
        linea (str)   |   ruta (str)
    """
    with open(ruta, "a") as archivo:
        archivo.write(linea)

def parsear_csv(datos:str)->list[dict]:
    """
    Función que transforma el texto leído de un CSV en una lista de diccionarios.
    La primera línea (encabezado) se usa como claves.

    Recibe como parámetro:
        datos (str)

    Retorna la lista de diccionarios.
    """
    datos_limpios = datos.strip()
    lista_lineas = datos_limpios.split("\n")
    encabezado = lista_lineas.pop(0)
    claves = encabezado.split(",")
    lista = []

    for i in range(len(lista_lineas)):
        dicc = {}
        valores = lista_lineas[i].split(",")
        for j in range(len(claves)):
            dicc.update({claves[j]:valores[j]})
        lista.append(dicc)

    return lista

def guardar_partida_ranking(nombre:str, puntaje:int, ruta:str = RUTA_RANKING)->None:
    """
    Función que guarda el resultado de una partida en el archivo del ranking.
        - Si el archivo no existe, lo crea con el encabezado "nombre,puntaje".
        - Después agrega la línea nueva con modo "a" (no se pierde lo anterior).

    Recibe como parámetros:
        nombre (str)   |   puntaje (int)   |   ruta (str) = "ranking.csv"
    """
    datos = leer_archivo_csv(ruta)
    if datos == None or datos.strip() == "":
        escribir_archivo("nombre,puntaje\n", ruta)

    linea = nombre + "," + str(puntaje) + "\n"
    anexar_linea(linea, ruta)

def buscar_jugador(jugadores:list[dict], nombre:str)->int:
    """
    Función que busca un jugador por nombre dentro de la lista de jugadores.

    Recibe como parámetros:
        jugadores (list[dict])   |   nombre (str)

    Retorna el índice donde está el jugador, o -1 si no está.
    """
    indice = -1
    for i in range(len(jugadores)):
        if jugadores[i]["nombre"] == nombre:
            indice = i
            break
    return indice

def obtener_mejores_puntajes(partidas:list[dict])->list[dict]:
    """
    Función que recorre todas las partidas guardadas y deja a cada jugador UNA sola vez,
    con el MAYOR de sus puntajes (los nombres en el ranking son irrepetibles).

    Recibe como parámetro:
        partidas (list[dict])

    Retorna una lista de diccionarios {"nombre": str, "puntaje": int} sin nombres repetidos.
    """
    jugadores = []
    for partida in partidas:
        nombre = partida["nombre"]
        puntaje = int(partida["puntaje"])
        indice = buscar_jugador(jugadores, nombre)

        if indice == -1:
            jugadores.append({"nombre":nombre, "puntaje":puntaje})
        elif puntaje > jugadores[indice]["puntaje"]:
            jugadores[indice]["puntaje"] = puntaje

    return jugadores

def intercambiar_elementos(lista:list, i:int, j:int)->None:
    """
    Función que intercambia dos elementos de una lista a través de sus índices.

    Recibe como parámetros:
        lista (list)   |   i (int)   |   j (int)
    """
    aux = lista[j]
    lista[j] = lista[i]
    lista[i] = aux

def ordenar_ranking_desc(jugadores:list[dict])->None:
    """
    Función que ordena la lista de jugadores por puntaje de forma DESCENDENTE (burbujeo).

    Recibe como parámetro:
        jugadores (list[dict])
    """
    for i in range(len(jugadores) - 1):
        for j in range(i + 1, len(jugadores)):
            if jugadores[i]["puntaje"] < jugadores[j]["puntaje"]:
                intercambiar_elementos(jugadores, i, j)

def mostrar_ranking(ruta:str = RUTA_RANKING)->None:
    """
    Función que muestra el top 10 de jugadores con su puntaje máximo,
    ordenados de forma descendente.
    Pasos: leer archivo -> parsear CSV -> dejar el mejor puntaje de cada uno -> ordenar -> mostrar.

    Recibe como parámetro:
        ruta (str) = "ranking.csv"
    """
    datos = leer_archivo_csv(ruta)

    print("#----------------------------------------#\n")
    print("          Ranking de jugadores")
    print("\n#----------------------------------------#")

    if datos == None:
        print("Todavía no hay partidas registradas.")
    else:
        partidas = parsear_csv(datos)
        jugadores = obtener_mejores_puntajes(partidas)
        ordenar_ranking_desc(jugadores)

        if len(jugadores) == 0:
            print("Todavía no hay partidas registradas.")
        else:
            print("Posición   Jugador          Puntaje")
            print("#----------------------------------------#")
            cantidad = len(jugadores)
            if cantidad > 10:
                cantidad = 10
            for i in range(cantidad):
                posicion = str(i + 1) + "."
                nombre = jugadores[i]["nombre"]
                print(posicion + " " * (11 - len(posicion)) + nombre + " " * (17 - len(nombre)) + str(jugadores[i]["puntaje"]))

    print("#----------------------------------------#")
    input("Presionar {Enter} para volver al menú principal: ")
    limpiar_teclado_os()


#--------------------------------------------------------#
# Otros
def limpiar_teclado_os()->None:
    """
    Objetivo: Función con el {import os} que al convocarlo sirve para limpiar el teclado según el OS del usuario sin necesidad de repetir código.
    """
    import os 

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")