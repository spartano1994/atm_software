from menu import *
from clients_data import *

def principal() :
    while True:
        print( "Bienvenido a Mexabank." )

        # Verificamos que se trate de un numero de tarjeta bien escrito
        card_number = validate_card_number()

        # Verificamos que exista un CSV con información de clientes, en caso contrario se crea una
        validate_database()

        # La variable client_data debe ser global pues la mandaremos por referencia a todas las funciones
        global client_data

        # Verificamos que el número de tarjeta válidado corresponda a un cliente y que su
        # tarjeta no esté bloqueada, si lo está, retira la tarjeta y comienza de nuevo
        message_validation , client_data , index = validate_client_data( card_number )

        if message_validation != "valid_card" :
            del client_data
            continue

        # Si la tarjeta no ha sido bloqueada, preguntamos por la contraseña
        status_pass = validate_password( client_data )

        if status_pass == "locked_card" :
            del client_data
            continue
        elif status_pass == "exit_option" :
            del client_data
            bye()
            continue

        principal_menu()

        bye()

        break


if __name__ == "__main__" :
    principal()