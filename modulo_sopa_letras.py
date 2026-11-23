#---------#     Módulo que contiene la Sopa de Letras del TP_3 de Programación I   #---------#

# Módulos que importo
import random as r
from modulo_tragamonedas import validar_apuesta_min_max


#--------------------------------------------------------#
# Función que incia el juego la sopa de letras
def iniciar_sopa_letras(saldo:int, apuesta:int)->int:
    """
    Función que inicia el juego de Sopa de Letras.

    Recibe el parámetro:
        saldo (int)     |     apuesta(int)
    
    Retorna el saldo modificado.
    """
    # Declaro la lista con las palabras a utilizar:
    palabras_disponibles = ["PROGRAMACION", "TUPLAS", "LISTAS",
                            "DICCIONARIOS", "MODULO", "CODIGO",
                            "METODOS", "PYTHON", "MATRIZ",
                            "BOOLEANO", "ARCHIVO", "VARIABLE",
                            "BURBUJA", "FUNCION", "CADENA"]

    cant_filas = 15
    cant_columnas = 15
    cant_palabras = 10
    intentos = 12
    palabras_encontradas = []
    mensaje = ""

    # Interfaz de bienvenida
    print("#----------------------------------------#\n")
    print("   ¡¡Bienvenido a la Sopa de Letras!!")
    print("\n#----------------------------------------#")
    print(f"Su Saldo es de {saldo}$.")
    print(f"Su Apuesta Actual es de {apuesta}$.")
    print("#----------------------------------------#")
    input("Presionar el botón {Enter} para empezar a jugar: ")
    limpiar_teclado_os()

    # Validación de la apuesta y descuento del saldo
    apuesta = validar_apuesta_min_max(apuesta, saldo)
    saldo = saldo - apuesta

    # Preparación de la partida
    palabras_ocultas = seleccionar_palabras(palabras_disponibles, cant_palabras)
    matriz = generar_sopa_letras(cant_filas, cant_columnas, palabras_ocultas)

    # Desarrollo del juego
    while intentos > 0 and len(palabras_encontradas) < cant_palabras:
        limpiar_teclado_os()
        mostrar_sopa_letras(matriz)
        print("#----------------------------------------#")
        print(f"Palabras encontradas: {len(palabras_encontradas)}/{cant_palabras}")
        mostrar_lista(palabras_encontradas)
        print(f"Intentos restantes: {intentos}")
        print(f"Tu apuesta es de {apuesta}$.")
        print("#----------------------------------------#")
        if mensaje != "":
            print(mensaje)
            print("#----------------------------------------#")

        palabra = input("> Ingresá una palabra (o '0' para abandonar): ")
        palabra = palabra.strip().upper()

        if palabra == "0":
            mensaje = "Abandonaste la partida."
            break

        intentos -= 1

        if buscar_en_lista(palabras_encontradas, palabra) == True:
            mensaje = f"La palabra {palabra} ya la habías encontrado. Perdiste un intento."
        elif buscar_en_lista(palabras_ocultas, palabra) == True and marcar_palabra_en_matriz(matriz, palabra) == True:
            palabras_encontradas.append(palabra)
            mensaje = f"¡¡Bien!! Encontraste la palabra {palabra}."
        else:
            mensaje = f"La palabra {palabra} no está en la sopa de letras."

    # Fin de la partida: resultados
    if len(palabras_encontradas) == cant_palabras:
        mensaje = "¡¡Encontraste todas las palabras!!"
    elif intentos == 0:
        mensaje = mensaje + "\nSe terminaron tus intentos."

    limpiar_teclado_os()
    mostrar_sopa_letras(matriz)
    print("#----------------------------------------#")
    print(mensaje)
    print(f"Encontraste {len(palabras_encontradas)} de {cant_palabras} palabras.")
    mostrar_palabras_faltantes(palabras_ocultas, palabras_encontradas)

    premio = calcular_premio_sopa(len(palabras_encontradas), apuesta)
    saldo = saldo + premio

    print("#----------------------------------------#")
    if premio == 0:
        print(f"Perdiste la apuesta de {apuesta}$.")
    elif premio == apuesta:
        print(f"Recuperaste tu apuesta de {apuesta}$.")
    else:
        print(f"¡Ganaste {premio - apuesta}$ además de recuperar tu apuesta!")
    print(f"Tu saldo actual es de {saldo}$.")
    print("#----------------------------------------#")
    input("Presionar {Enter} para volver al menú principal: ")
    limpiar_teclado_os()

    return saldo


#--------------------------------------------------------#
# Funciones de matrices
def inicializar_matriz(cant_filas:int, cant_columnas:int, valor_inicial:any=None)->list[list]:
    """
    Función que crea una matriz con la cantidad de filas y columnas indicadas,
    con todas sus celdas cargadas con un valor inicial.

    Recibe como parámetros:
        cant_filas (int)   |   cant_columnas (int)   |   valor_inicial (any) = None

    Retorna la matriz creada.
    """
    matriz = []
    for _ in range(cant_filas):
        fila = []
        for _ in range(cant_columnas):
            fila += [valor_inicial]
        matriz += [fila]
    return matriz

def mostrar_sopa_letras(matriz:list[list])->None:
    """
    Función que muestra la sopa de letras por pantalla en filas y columnas.
    Las palabras ya encontradas se ven en minúscula.

    Recibe como parámetro:
        matriz (list[list])
    """
    print("#----------------------------------------#")
    for i in range(len(matriz)):
        print("   ", end="")
        for j in range(len(matriz[i])):
            print(matriz[i][j], end=" ")
        print()


#--------------------------------------------------------#
# Funciones para preparar la partida de la sopa de letras
def buscar_en_lista(lista:list, valor:any)->bool:
    """
    Función que busca un valor dentro de una lista.

    Recibe como parámetros:
        lista (list)   |   valor (any)

    Retorna True si el valor está en la lista, False si no está.
    """
    retorno = False
    for i in range(len(lista)):
        if lista[i] == valor:
            retorno = True
            break
    return retorno

def seleccionar_palabras(palabras_disponibles:list, cantidad:int)->list:
    """
    Función que selecciona al azar una cantidad de palabras de la colección,
    sin que se repitan.

    Recibe como parámetros:
        palabras_disponibles (list)   |   cantidad (int)

    Retorna una lista con las palabras seleccionadas.
    """
    seleccionadas = []
    while len(seleccionadas) < cantidad:
        palabra = palabras_disponibles[r.randint(0, len(palabras_disponibles) - 1)]
        if buscar_en_lista(seleccionadas, palabra) == False:
            seleccionadas.append(palabra)
    return seleccionadas

def generar_sopa_letras(cant_filas:int, cant_columnas:int, palabras:list)->list[list]:
    """
    Función que genera la matriz de la sopa de letras: ubica las palabras
    y completa las celdas vacías con letras mayúsculas al azar.
    Si alguna palabra no se pudo ubicar, vuelve a armar la matriz desde cero.

    Recibe como parámetros:
        cant_filas (int)   |   cant_columnas (int)   |   palabras (list)

    Retorna la matriz completa.
    """
    todas_ubicadas = False
    while todas_ubicadas == False:
        matriz = inicializar_matriz(cant_filas, cant_columnas, " ")
        todas_ubicadas = True
        for palabra in palabras:
            if ubicar_palabra(matriz, palabra) == False:
                todas_ubicadas = False
                break

    completar_celdas_vacias(matriz)
    return matriz

def ubicar_palabra(matriz:list[list], palabra:str)->bool:
    """
    Función que intenta ubicar una palabra en una posición y dirección al azar
    (0 = horizontal de izquierda a derecha | 1 = vertical de arriba hacia abajo).
    Prueba hasta 100 veces.

    Recibe como parámetros:
        matriz (list[list])   |   palabra (str)

    Retorna True si la pudo ubicar, False si no.
    """
    ubicada = False
    intentos = 0
    while ubicada == False and intentos < 100:
        direccion = r.randint(0, 1)
        if direccion == 0:
            fila = r.randint(0, len(matriz) - 1)
            columna = r.randint(0, len(matriz[0]) - len(palabra))
        else:
            fila = r.randint(0, len(matriz) - len(palabra))
            columna = r.randint(0, len(matriz[0]) - 1)

        if verificar_espacio(matriz, palabra, fila, columna, direccion) == True:
            escribir_palabra(matriz, palabra, fila, columna, direccion)
            ubicada = True
        intentos += 1
    return ubicada

def verificar_espacio(matriz:list[list], palabra:str, fila:int, columna:int, direccion:int)->bool:
    """
    Función que verifica si una palabra entra en la posición indicada:
    cada celda tiene que estar vacía o tener la misma letra (cruce de palabras).

    Recibe como parámetros:
        matriz (list[list])   |   palabra (str)   |   fila (int)   |   columna (int)   |   direccion (int)

    Retorna True si hay lugar, False si no.
    """
    retorno = True
    for k in range(len(palabra)):
        if direccion == 0:
            celda = matriz[fila][columna + k]
        else:
            celda = matriz[fila + k][columna]
        if celda != " " and celda != palabra[k]:
            retorno = False
            break
    return retorno

def escribir_palabra(matriz:list[list], palabra:str, fila:int, columna:int, direccion:int)->None:
    """
    Función que escribe la palabra, letra por letra, dentro de la matriz.

    Recibe como parámetros:
        matriz (list[list])   |   palabra (str)   |   fila (int)   |   columna (int)   |   direccion (int)
    """
    for k in range(len(palabra)):
        if direccion == 0:
            matriz[fila][columna + k] = palabra[k]
        else:
            matriz[fila + k][columna] = palabra[k]

def completar_celdas_vacias(matriz:list[list])->None:
    """
    Función que completa las celdas vacías con letras mayúsculas al azar (A-Z).
    Usa los códigos ASCII: 65 = 'A' y 90 = 'Z'.

    Recibe como parámetro:
        matriz (list[list])
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == " ":
                matriz[i][j] = chr(r.randint(65, 90))


#--------------------------------------------------------#
# Funciones para el desarrollo de la sopa de letras
def marcar_palabra_en_matriz(matriz:list[list], palabra:str)->bool:
    """
    Función que busca la palabra en la matriz en sentido horizontal y vertical.
    Si la encuentra, la pasa a minúscula para que el jugador la vea marcada.

    Recibe como parámetros:
        matriz (list[list])   |   palabra (str)

    Retorna True si la encontró, False si no.
    """
    encontrada = False

    # Búsqueda horizontal
    for i in range(len(matriz)):
        for j in range(len(matriz[i]) - len(palabra) + 1):
            if coincide_palabra(matriz, palabra, i, j, 0) == True:
                for k in range(len(palabra)):
                    matriz[i][j + k] = matriz[i][j + k].lower()
                encontrada = True
                break
        if encontrada == True:
            break

    # Búsqueda vertical (solo si no la encontró en horizontal)
    if encontrada == False:
        for i in range(len(matriz) - len(palabra) + 1):
            for j in range(len(matriz[i])):
                if coincide_palabra(matriz, palabra, i, j, 1) == True:
                    for k in range(len(palabra)):
                        matriz[i + k][j] = matriz[i + k][j].lower()
                    encontrada = True
                    break
            if encontrada == True:
                break

    return encontrada

def coincide_palabra(matriz:list[list], palabra:str, fila:int, columna:int, direccion:int)->bool:
    """
    Función que compara, letra por letra, la palabra con la matriz desde una posición.
    Usa .upper() para que coincida también con letras ya marcadas en minúscula.

    Recibe como parámetros:
        matriz (list[list])   |   palabra (str)   |   fila (int)   |   columna (int)   |   direccion (int)

    Retorna True si coincide, False si no.
    """
    retorno = True
    for k in range(len(palabra)):
        if direccion == 0:
            letra = matriz[fila][columna + k]
        else:
            letra = matriz[fila + k][columna]
        if letra.upper() != palabra[k]:
            retorno = False
            break
    return retorno

def mostrar_palabras_faltantes(palabras_ocultas:list, palabras_encontradas:list)->None:
    """
    Función que muestra las palabras ocultas que el jugador no encontró.

    Recibe como parámetros:
        palabras_ocultas (list)   |   palabras_encontradas (list)
    """
    faltantes = []
    for palabra in palabras_ocultas:
        if buscar_en_lista(palabras_encontradas, palabra) == False:
            faltantes.append(palabra)

    if len(faltantes) > 0:
        print("Las palabras que te faltaron eran:")
        for palabra in faltantes:
            print(f"  - {palabra}")


#--------------------------------------------------------#
# Función del sistema de apuestas
def calcular_premio_sopa(cant_encontradas:int, apuesta:int)->int:
    """
    Función que calcula cuánto dinero recibe el jugador según las palabras encontradas
    (la apuesta ya se descontó al empezar, por eso el premio incluye recuperarla):
        0 o 1   -> Pierde la apuesta        (recibe 0)
        2 o 3   -> Recupera la apuesta      (recibe apuesta)
        4 o 5   -> Gana 50% adicional       (recibe apuesta + 50%)
        6 o 7   -> Gana 100% adicional      (recibe apuesta * 2)
        8 o 9   -> Gana 150% adicional      (recibe apuesta * 2 + 50%)
        10      -> Gana 200% adicional      (recibe apuesta * 3)

    Recibe como parámetros:
        cant_encontradas (int)   |   apuesta (int)

    Retorna el premio (int).
    """
    if cant_encontradas <= 1:
        premio = 0
    elif cant_encontradas <= 3:
        premio = apuesta
    elif cant_encontradas <= 5:
        premio = apuesta + apuesta // 2
    elif cant_encontradas <= 7:
        premio = apuesta * 2
    elif cant_encontradas <= 9:
        premio = apuesta * 2 + apuesta // 2
    else:
        premio = apuesta * 3
    return premio


#--------------------------------------------------------#
# Función para mostrar listas
def mostrar_lista(lista:list)->None:
    """
    Función que muestra cada elemento de una lista, uno debajo del otro.
    Si la lista está vacía, no muestra nada.

    Recibe como parámetro:
        lista (list)
    """
    for i in range(len(lista)):
        print(f"  - {lista[i]}")


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