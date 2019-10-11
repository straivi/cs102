def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    keyword = keyword.lower()
    ciphertext = ''
    for i in range(len(plaintext)):
        symbol = plaintext[i]
        if ord(symbol) > 122 or ord(symbol) < 65 or 90 < ord(symbol) < 97:
            ciphertext += symbol
        else:
            if 65 <= ord(symbol) <= 90:
                newKey = ord(symbol) + ord(keyword[i % len(keyword)]) - 97
                if newKey > 90:
                    newKey -= 26
            else:
                newKey = ord(symbol) + ord(keyword[i % len(keyword)]) - 97
                if newKey > 122:
                    newKey -= 26
            ciphertext += chr(newKey)
    
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    keyword = keyword.lower()
    plaintext = ''
    for i in range(len(ciphertext)):
        symbol = ciphertext[i]
        if ord(symbol) > 122 or ord(symbol) < 65 or 90 < ord(symbol) < 97:
            plaintext += symbol
        else:
            if 65 <= ord(symbol) <= 90:
                newKey = ord(symbol) + 97 - ord(keyword[i % len(keyword)])
                if newKey < 65:
                    newKey += 26
            else:
                newKey = ord(symbol) + 97 - ord(keyword[i % len(keyword)])
                if newKey < 97:
                    newKey += 26
            plaintext += chr(newKey)
    return plaintext
