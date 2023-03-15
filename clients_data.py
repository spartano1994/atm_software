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
                           "card_state" : [ 1 , 1 , 0 ] ,
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

    # Verificamos que el número de tarjeta esté e la columna de números card_number_data
    if card_number_modified in card_number_data :
        # Encontramos los datos correspondientes al número de tarjeta y solo nos quedamos con ciertos datos
        find = np.where( database[ "card_number" ] == card_number_modified )
        index = int( find[ 0 ][ 0 ])
        client_data = database.loc[ index, [ "client_number", "password" , "card_state" , "total_balance" , "day_balance" ] ]

        # Verificamos que la tarjeta no esté bloqueada( 0 )
        if client_data[ "card_state" ] == 0:
            print("Su tarjeta se encuentra bloqueada\nConsulte a su banco")

            time.sleep( 5 )
            os.system( "cls" )
            return "locked_card", np.NaN, np.NaN

        return "valid_card", client_data, index

    # Si no está simplemente pedimos que remueva la tarjeta
    else:
        print( "Tarjeta inválida" )
        print( "Remueva su tarjeta e intente de nuevo" )

        del database
        time.sleep( 5 )
        os.system( "cls" )

        return "invalid_card", np.NaN, np.NaN
    

def validate_password( client_data ) :
    """Esta función le pide la contraseña al usuario, si se equivoca después de 5 intentos, la tarjeta
        quedará bloqueada (card_status=0)"""

    # El usuario tiene 5 intentos para colocar correctamente su contraseña
    attemps = 5

    while True:
        # Pedimos al usuario que ingrese su contraseña
        password = input( "Ingrese su contraseña o presione enter para salir:\n " )

        # Si el password es correcto salimos de esta función para pasar al menu d usuario
        if password == client_data[ "password" ] :
            return "valid_pass"

        if len( password ) == 0 :
            return "exit_option"

        # Si la contraseña no es correcta, le informamos al usuario y le quitamos uno de los intentos
        print( "Contraseña incorrecta. Intente de nuevo." )
        attemps -= 1

        # si falla 5 veces, su tarjeta queda bloqeada
        if attemps == 0 :
            print( "Su tarjeta ha sido bloqueada. Ha colocado incorrectamente su contraseña 5 vcces." )
            print( "Consulte a su banco" )

            time.sleep( 5 )
            os.system( "cls" )
            return "locked_card"

        time.sleep( 3 )
        os.system( "cls" )


def balance_inquiry( client_data , index ) :
    """Esta función muestra el saldo total del usuario y su saldo ese día"""
    os.system( "cls" )

    # Se importa el csv con los clientes
    ruta_csv = os.getcwd()
    ruta_csv += "\clientsdata.csv"
    database = pd.read_csv( ruta_csv )

    # Se imprime el saldo disponible para ese día y el saldo total de la cuenta
    print( "Saldo total = :" , database.loc[ index , "total_balance"  ] )
    print( "Saldo disponible = :" , database.loc[ index , "day_balance" ] )

    input( "Presione enter para coninuar" )


def cash_withdrawal( client_data , index ) :
    """Esta función efectúa los retiros de la cuenta una vez validada"""

    os.system( "cls" )

    # Se importa el csv con los clientes
    ruta_csv = os.getcwd()
    ruta_csv += "\clientsdata.csv"
    database = pd.read_csv( ruta_csv )

    # Se pide la cantidad a retirar y se verifica que sea menor o igual a la cantidad disponible ese día
    while True :
        cash = int( input( "Ingrese la cantidad que desea retirar :\n" ) )

        if cash < database.loc[ index , "day_balance" ] :
            break
        else :
            os.system( "cls" )
            print( "Esa cantidad no está disponible en este momento. Intente de nuevo" )

    # Se verifica que la cantidad a retirar esté disponible
    while True:
        if cash <= database.loc[ index , "total_balance" ]:

            # Se extraen los aldos totales y del día
            day_balance = float( database.loc[ index , "day_balance" ] )
            total_balance = float( database.loc[ index , "total_balance" ] )

            # Se resta la cantidad a retirar del saldo total y del día
            remaining_total = total_balance - float( cash )
            remaining_day = day_balance - float( cash )

            # Se reescriben los nuevos saldos totales y del día
            database.loc[ index , "day_balance" ] = remaining_day
            database.loc[ index , "total_balance" ] = remaining_total

            # Se guarda nuevamente el csv, el parámetro index se coloca porque, en caso de no hacerlo
            # escribe una columna nueva cada vez que se retire saldo
            database.to_csv( ruta_csv , index = False )
            
            # Se muestra por pantalla los saldos de la cuenta
            os.system( "cls" )
            print( "Su saldo es:" , remaining_total )
            print( "Su saldo disponible es:" , remaining_day )
            time.sleep( 6 )
            os.system( "cls" )
            break
        else:
            # Se anuncai que el saldo es insuficiente y se regresa a preguntar la cantidad a retirar
            print( "Saldo insuficiente" )
            print( "Intente de nuevo" )
            time.sleep( 4 )
            os.system( "cls" )


def wire_transfer( client_data , index ) :
    os.system( "cls" )

    # Se importa el csv con los clientes
    ruta_csv = os.getcwd()
    ruta_csv += "\clientsdata.csv"
    database = pd.read_csv( ruta_csv )

    # Se pide la cantidad a retirar y se verifica que sea menor o igual a la cantidad disponible ese día
    while True :
        cash = int( input( "Ingrese la cantidad que desea retirar :\n" ) )

        if cash < database.loc[ index , "day_balance" ] :
            break
        else :
            os.system( "cls" )
            print( "Esa cantidad no está disponible. Intente de nuevo" )


def validate_option( option , client_data , index ) :
        if option == "1" :
            balance_inquiry( client_data , index )
        elif option == "2" :
            cash_withdrawal( client_data , index )
        elif option == "3" :
            wire_transfer( client_data , index )
        else:
            pass
        