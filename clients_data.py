import pandas as pd
import os
import datetime as dt
import pytz
import time
import numpy as np

def validate_database() :
    """Esta función importa los datos de un csv con los datos de los clientes en caso de existir un csv, lo crea
     en caso de no existir y nos devuelve la ruta"""

    # Guardamos la zona horaria de la consulta
    zone = pytz.timezone( 'America/Mexico_City' )

    # Obtenemos la ruta de la carpeta en la que estamos trabajando y le añadimos el nombre y formato del csv
    ruta_csv = os.getcwd()
    ruta_csv += "\clientsdata.csv"

    # Verificamos si el csv existe, en caso contrario se crea uno para trabajar con él
    if os.path.exists( ruta_csv ) :
        pass
    else :
        # Se crea una variable con la fecha de hoy para agregarla al DataFrame
        today = dt.datetime.now()
        today = today.astimezone( zone )

        # Creamos los datos, el valor  en la columna card_state significa que la tarjeta está bloqueada
        client_columns = { "client_number" : [ "000001" , "000002" , "000003" ] ,
                           "card_number"  : [ "0000-0000-0000-0001" , "0000-0000-0000-0002" , "0000-0000-0000-0003"  ] ,
                           "complete_name" : [ "Juan Pérez Pérez" , "Leonardo Gabriel Díaz Feliciano" , "José Antonio García Gómez" ] ,
                           "password" : [ "password1" , "password2" , "password3" ]  ,
                           "card_state" : [ 1 , 1 , 1 ] ,
                           "total_balance" : [ 100000 , 100000 , 100000 ] ,
                           "day_balance" : [ 9100 , 9100 , 9100 ] ,
                           "last_consultation" : [ today , today , today ] }

        # Creamos un DataFrame y lo guardamos en un csv con la ruta construida
        df = pd.DataFrame( data = client_columns )
        df.to_csv( ruta_csv , encoding = "UTF-8" )

    return ruta_csv


def validate_client_data( card_number ) :
    """Esta función valida que el número de cuenta ingresado se encuentre en la base de datos
    Args:
        card_number (str): Número de la tarjeta.

    Returns:
        (tuple): Tupla con 3 entradas, validación( str ), los datos del usuario ( np.series ) y el
        índice donde se encontraron ( int )
    """

    # Se importa el csv con los clientes
    ruta_csv = os.getcwd()
    ruta_csv += "\clientsdata.csv"

    # Extraemos solo los número de las tarjetas
    database = pd.read_csv( ruta_csv )
    card_number_data = database[ "card_number" ].to_numpy()

    # Construimos una columna con los números de tarjeta en un array de numpy
    card_number_modified = card_number[0: 4] + "-" + card_number[4: 8] + "-" + card_number[8: 12] + "-" + card_number[12: 16]

    if card_number_modified in card_number_data :
        # Encontramos los datos correspondientes al número de tarjeta y solo nos quedamos con ciertos datos
        find = np.where( database[ "card_number" ] == card_number_modified )
        index = int( find[ 0 ][ 0 ])
        client_data = database.loc[ index, [ "client_number", "password" , "card_state" , "total_balance" , "day_balance" ] ]

        # Verificamos que la tarjeta no esté bloqueada( 0 )
        if client_data[ "card_state" ] == 0:
            print("Su tarjeta ha sido bloqueada\nConsulte a su banco")

            time.sleep( 5 )
            os.system( "cls" )
            return "locked_card", np.NaN, np.NaN

        return "valid_card", client_data, index

    else:
        print( "Tarjeta inválida" )
        print( "Remueva su tarjeta e intente de nuevo" )

        del data
        time.sleep( 5 )
        os.system( "cls" )

        return "invalid_card", np.NaN, np.NaN
