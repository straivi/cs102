def encrypt_caesar(plaintext, shift):
    resaultText = ''
    shift = shift % 26
    for simbol in plaintext:
        if ord(simbol) > 122 or ord(simbol) < 65 or 90 < ord(simbol) < 97:
            resaultText += simbol
        else: 
            if 65 <= ord(simbol) <= 90:
                newKey = ord(simbol) + shift
                if newKey > 90:
                    newKey -= 26
            else:
                newKey = ord(simbol) + shift
                if newKey > 122:
                    newKey -= 26        
            resaultText += chr(newKey)
    return resaultText



def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    #return plaintext


    

