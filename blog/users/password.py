####################################################
# FUNCTION TO CHECK IF A PASSWORD IS STRONG ########
####################################################

def is_strong(password):
    upper = False
    lower = False
    symbol = False
    number = False

    if (len(password) < 6):
        return False

    for char in password:
        if (char.isdigit()):
            number = True
        elif (char.isupper()):
            upper = True
        elif (char.islower()):
            lower = True
        elif (not char.isalnum()):
            symbol = True
        
        if (upper and lower and symbol and number):
            return True
    
    return False
