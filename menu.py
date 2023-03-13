import os
import re

def validate_card_number( ):
    """Revisa que el número de tarjeta esté bien escrito"""
    while True:
        os.system( "cls" )
        # Pedimos al usuario que inserte su tarjeta
        card_number = input( "Inserte su tarjeta: " )
        patron = r"\d{16}"
        validate = re.fullmatch( patron , card_number )

        if validate == None :
            print( "Intente de nuevo" )
        else:
            return card_number
