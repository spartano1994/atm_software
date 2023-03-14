import os
import re
import time


def validate_card_number( ):
    """Revisa que el número de tarjeta esté bien escrito"""
    validate = None

    while validate == None:
        os.system( "cls" )

        
        # Pedimos al usuario que inserte su tarjeta
        card_number = input( "Inserte su tarjeta: " )
        patron = r"\d{16}"
        validate = re.fullmatch( patron , card_number )

        if validate == None :
            print( "Intente de nuevo" )
            time.sleep( 3 )
        else:
            return card_number

def principal_menu() :
    os.system( "cls" )

    print( """Teclea la opción que deseas realizar
        1.- Consulta de saldo
        2.- Retiro de efectivo
        3.- Transferenca bancaria
        4.- Salir""")

    option = input()

    return option

def bye() :
    print("Fue un placer atenderte")
    time.sleep( 3 )
    os.system("cls")
    print( "Vuelve pronto" )
    time.sleep( 3 )
    os.system( "cls" )
