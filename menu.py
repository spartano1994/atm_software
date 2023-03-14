import os
import re
import time


def validate_card_number( ):
    """Revisa que el número de tarjeta esté bien escrito
    
    Returns:
        card_number (str): Número de tarjeta válido
    """
    validate = None

    while validate == None:
        os.system( "cls" )
        print( "*****Bienvenido a Mexabank.*****" )

        # Pedimos al usuario que inserte su tarjeta
        card_number = input( "Inserte su tarjeta: " )

        # Establecemos que deba ser únicamente 16 dígitos
        patron = r"\d{16}"

        # Matcheamos la contraseña ingresada y el patrón de los 16 dígitos
        validate = re.fullmatch( patron , card_number )

        # Si no concidieron, habrá que intentar de nuevo
        if validate == None :
            print( "Intente de nuevo" )
            time.sleep( 3 )
        
        # Si coinciden, se sale de la función devolviendo el número de tarjeta
        else:
            return card_number


def user_menu() :
    os.system( "cls" )

    while True:
        print( """Teclea la opción que deseas realizar
            1.- Consulta de saldo
            2.- Retiro de efectivo
            3.- Transferenca bancaria
            4.- Salir""")

        option = input()

        if option in [ "1" , "2" , "3" , "4" ] :
            return option
        else:
            print( "opción inválida. Intente de nuevo" )
            time.sleep( 3 )


def bye() :
    """Esta función despide al usuario antes de dinalizar su sesión"""
    print("Fue un placer atenderte")
    time.sleep( 3 )
    os.system("cls")
    print( "Vuelve pronto" )
    time.sleep( 3 )
    os.system( "cls" )
