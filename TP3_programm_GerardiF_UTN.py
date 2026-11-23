#---------------------------- Trabajo Práctico 3 de Francisco Gerardi ----------------------------#

# TP_3 n°1: Buenas Profe y Fausto, acá le hago entrega del tercer trabajo práctico. Tengo una sola consulta,
#           creo que en lineas generales anda muy bien el programa, pero tengo un problema con el tema del archivo;
#           cada vez que cambio un modo de juego me guarda en el ranking el puntaje, haciendo que se guarde varias veces
#           el mismo nombre con distintos puntajes, en lugar de guardarlo una vez sola con el puntaje más alto. 
#           Desde ya, muchas gracias. Buenos días, tardes o noches.


# Importo el módulo con las funciones a utilizar:
from modulo_tragamonedas import iniciar_tragamonedas_virtual
from modulo_tragamonedas import validar_apuesta_min_max
from modulo_tragamonedas import limpiar_teclado_os
from modulo_blackjack import iniciar_blackjack
from modulo_sopa_letras import iniciar_sopa_letras
from modulo_ranking import pedir_nombre_jugador
from modulo_ranking import guardar_partida_ranking
from modulo_ranking import mostrar_ranking

#-----------------------------------------------------#
# Declaro el saldo y la apuesta inicial (compartidos por los 3 juegos)
saldo = 100
apuesta = 10

#-----------------------------------------------------#
# Pido el nombre del jugador al iniciar el programa
limpiar_teclado_os()
print("#----------------------------------------#\n")
print("        Bienvenido al Casino UTN")
print("\n#----------------------------------------#")
nombre_jugador = pedir_nombre_jugador()
limpiar_teclado_os()

#-----------------------------------------------------#
# Bucle while que se repite hasta salir del programa o quedarse sin saldo:
while saldo > 0:

#-----------------------------------------------------#
# Interfaz del menú principal:
    print("#----------------------------------------#\n")
    print("     Bienvenido al menú principal")
    print("\n#----------------------------------------#")
    print(f"Jugador: {nombre_jugador}")
    print("Modos seleccionables:\n")
    print("[1] Jugar Tragamonedas.")
    print("[2] Jugar Black Jack.")
    print("[3] Jugar Sopa de Letras.")
    print("[4] Cambiar Apuesta.")
    print("[5] Mostrar Ranking.")
    print("[6] Salir.")
    print("\n#----------------------------------------#")
    print(f"Su saldo actual es de [{saldo}]$.")
    print(f"Su apuesta actual es de [{apuesta}]$.")
    print("#----------------------------------------#\n")

    juego_select = input("> Modo seleccionado: ")

    match juego_select:

# Juego del Tragamonedas virtual:
        case "1":
            limpiar_teclado_os()
            saldo = iniciar_tragamonedas_virtual(saldo, apuesta)
            guardar_partida_ranking(nombre_jugador, saldo)

# Juego del Black Jack:
        case "2":
            limpiar_teclado_os()
            saldo = iniciar_blackjack(saldo, apuesta)
            guardar_partida_ranking(nombre_jugador, saldo)

# Juego de la Sopa de Letras:
        case "3":
            limpiar_teclado_os()
            saldo = iniciar_sopa_letras(saldo, apuesta)
            guardar_partida_ranking(nombre_jugador, saldo)

# Cambiar apuesta para jugar:
        case "4":
            print("\n#----------------------------------------#\n")
            apuesta = int(input("Cantidad de dinero a apostar: "))
            apuesta = validar_apuesta_min_max(apuesta, saldo)
            limpiar_teclado_os()

# Mostrar el ranking (top 10 leído desde el archivo):
        case "5":
            limpiar_teclado_os()
            mostrar_ranking()

# Salir del programa desde el menú principal:
        case "6":
            limpiar_teclado_os()
            print("Saliendo del programa...")
            break

# En caso de que el usuario coloque otro valor distinto a los del menú:
        case _:
            limpiar_teclado_os()
            print("#----------------------------------------#")
            print("Por favor, seleccionar una opción válida.")


#-----------------------------------------------------#
# Fin del programa
if saldo <= 0:
    print("#----------------------------------------#")
    print("Te quedaste sin saldo...")


print("#----------------------------------------#\n")
print(f"             Fin del programa")
print("\n#----------------------------------------#")
print(f" Gracias por jugar, {nombre_jugador}.")