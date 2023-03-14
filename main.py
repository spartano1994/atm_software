from menu import *
from clients_data import *

def principal() :
    while True:
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

        # Si falla 5 veces la contraseña, la tarjeta se bloquee. Si se desea salir antes de bloquear la tarjeta, simplemente se sale
        if status_pass == "locked_card" :
            del client_data
            continue
        elif status_pass == "exit_option" :
            del client_data
            bye()
            continue

        # Si todos los datos son correctos, se despliega el menu de usuario
        option = user_menu()
        validate_option( option , client_data = client_data , index = index )

        bye()

        break


if __name__ == "__main__" :
    principal()