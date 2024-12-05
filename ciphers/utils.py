def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)
    

def vigenere_encrypt(text, key):
    encrypted_text = []
    key_length = len(key)
    key_index = 0

    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            key_char = key[key_index % key_length].upper() if char.isupper() else key[key_index % key_length].lower()
            shift = ord(key_char) - ord('A') if char.isupper() else ord(key_char) - ord('a')
            encrypted_text.append(chr((ord(char) - base + shift) % 26 + base))
            key_index += 1
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)

def vigenere_decrypt(text, key):
    decrypted_text = []
    key_length = len(key)
    key_index = 0

    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            key_char = key[key_index % key_length].upper() if char.isupper() else key[key_index % key_length].lower()
            shift = ord(key_char) - ord('A') if char.isupper() else ord(key_char) - ord('a')
            decrypted_text.append(chr((ord(char) - base - shift) % 26 + base))
            key_index += 1
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)