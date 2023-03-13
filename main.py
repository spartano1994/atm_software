from menu import *
from clients_data import *

def principal() :
    card_number = validate_card_number()
    validate_database()
    message_validation , client_data , index = validate_client_data( card_number )

    print( message_validation )





if __name__ == "__main__" :
    principal()