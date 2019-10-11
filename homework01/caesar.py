<<<<<<< HEAD
def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    resaultText = ''
    shift = 3
    for simbol in plaintext:
        if ord(simbol) > 122 or ord(simbol) < 65 or 90 < ord(simbol) < 97:
            resaultText += simbol
        else:
=======
def encrypt_caesar(plaintext, shift):
    resaultText = ''
    shift = shift % 26
    for simbol in plaintext:
        if ord(simbol) > 122 or ord(simbol) < 65 or 90 < ord(simbol) < 97:
            resaultText += simbol
        else: 
>>>>>>> feature/caesar
            if 65 <= ord(simbol) <= 90:
                newKey = ord(simbol) + shift
                if newKey > 90:
                    newKey -= 26
            else:
                newKey = ord(simbol) + shift
                if newKey > 122:
<<<<<<< HEAD
                    newKey -= 26
=======
                    newKey -= 26        
>>>>>>> feature/caesar
            resaultText += chr(newKey)
    return resaultText


<<<<<<< HEAD
=======

>>>>>>> feature/caesar
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
<<<<<<< HEAD
    resaultText = ''
    shift = 3
    for simbol in ciphertext:
        if ord(simbol) > 122 or ord(simbol) < 65 or 90 < ord(simbol) < 97:
            resaultText += simbol
        else:
            if 65 <= ord(simbol) <= 90:
                newKey = ord(simbol) - shift
                if newKey < 65:
                    newKey += 26
            else:
                newKey = ord(simbol) - shift
                if newKey < 97:
                    newKey += 26
            resaultText += chr(newKey)
    return resaultText
=======
    # PUT YOUR CODE HERE
    #return plaintext


    

>>>>>>> feature/caesar
