from django.shortcuts import render
from .models import CaesarCipherData
from .utils import caesar_encrypt, caesar_decrypt,vigenere_encrypt, vigenere_decrypt
from django.http import JsonResponse

# Create your views here.
#MARK: Caesar Cipher
def caesar_cipher_view(request):
    result = None
    opposite_result = None
    operation_label = None
    opposite_operation_label = None
    data_label = None

    # Caesar cipher explanation text
    caesar_explanation = """
    The Caesar Cipher is a substitution cipher where each letter in the plaintext is replaced by a letter with a fixed number of positions down or up the alphabet. 
    For example, with a shift of 3:
    A becomes D, B becomes E, C becomes F, and so on. 
    The cipher works by rotating the alphabet, so when the shift goes beyond 'Z', it starts from 'A' again.
    """

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        shift_raw = request.POST.get("shift", "").strip()
        operation = request.POST.get("operation", "")
        cipher = request.POST.get("cipher", "caesar")

        # Validate shift input
        if not shift_raw.isdigit():
            return render(request, "ciphers/caesar_cipher.html", {
                "error": "Key must be a valid integer.",
                "text": text,
                "shift": shift_raw,
                "cipher": cipher,
                "operation": operation,
                "caesar_explanation": caesar_explanation  # Pass the explanation to the template
            })
        
        shift = int(shift_raw)

        if cipher == "caesar":
            if operation == "encrypt":
                result, _ = caesar_encrypt_with_steps(text, shift)
                opposite_result, _ = caesar_decrypt_with_steps(result, shift)
                operation_label = "Encryption"
                opposite_operation_label = "Decryption"
                data_label = f"Data to be decrypted: {result}"
            elif operation == "decrypt":
                result, _ = caesar_decrypt_with_steps(text, shift)
                opposite_result, _ = caesar_encrypt_with_steps(result, shift)
                operation_label = "Decryption"
                opposite_operation_label = "Encryption"
                data_label = f"Data to be encrypted: {result}"

        return render(request, "ciphers/caesar_cipher.html", {
            "text": text,
            "shift": shift,
            "cipher": cipher,
            "operation": operation,
            "operation_label": operation_label,
            "opposite_operation_label": opposite_operation_label,
            "data_label": data_label,
            "result": result,
            "opposite_result": opposite_result,
            "caesar_explanation": caesar_explanation  # Pass explanation
        })

    return render(request, "ciphers/caesar_cipher.html", {
        "caesar_explanation": caesar_explanation  # Pass explanation in case no POST request
    })


def caesar_encrypt_with_steps(text, shift):
    steps = []
    encrypted_text = []
    for i, char in enumerate(text):
        if char.isalpha():
            base = 65 if char.isupper() else 97
            shifted = (ord(char) - base + shift) % 26 + base
            encrypted_text.append(chr(shifted))
            steps.append(f"Step {i+1}: '{char}' shifted by {shift} to '{chr(shifted)}'")
        else:
            encrypted_text.append(char)
            steps.append(f"Step {i+1}: Non-alphabetic character '{char}' remains unchanged")
    return ''.join(encrypted_text), steps


def caesar_decrypt_with_steps(text, shift):
    steps = []
    decrypted_text = []
    for i, char in enumerate(text):
        if char.isalpha():
            base = 65 if char.isupper() else 97
            shifted = (ord(char) - base - shift) % 26 + base
            decrypted_text.append(chr(shifted))
            steps.append(f"Step {i+1}: '{char}' shifted back by {shift} to '{chr(shifted)}'")
        else:
            decrypted_text.append(char)
            steps.append(f"Step {i+1}: Non-alphabetic character '{char}' remains unchanged")
    return ''.join(decrypted_text), steps


def update_opposite_result(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        cipher = data.get("cipher")
        operation = data.get("operation")
        
        text = "Your Example Text"  # Replace with actual logic if needed
        shift = 3  # Example shift value

        opposite_result = ""
        steps = []
        opposite_operation_label = None
        data_label = None
        
        if cipher == "caesar":
            if operation == "encrypt":
                opposite_result, steps = caesar_decrypt_with_steps(text, shift)
                opposite_operation_label = "Decryption"
                data_label = f"Data to be decrypted: {text}"
            elif operation == "decrypt":
                opposite_result, steps = caesar_encrypt_with_steps(text, shift)
                opposite_operation_label = "Encryption"
                data_label = f"Data to be encrypted: {text}"

        return JsonResponse({
            "result": opposite_result,
            "steps": steps,
            "opposite_operation_label": opposite_operation_label,
            "data_label": data_label
        })


#MARK: Vigenere Cipher
# def vigenere_cipher_view(request):
#     result = None
#     opposite_result = None
#     operation_label = None
#     opposite_operation_label = None
#     data_label = None

#     # Vigenère cipher explanation text
#     vigenere_explanation = """
#     The Vigenère Cipher is a method of encrypting alphabetic text by using a simple form of polyalphabetic substitution. 
#     A key word is repeated over the plaintext, and each letter is shifted by the position of the corresponding letter in the key.
#     For example, with the key 'KEY' and plaintext 'HELLO':
#     'H' shifted by 'K' (position 10) becomes 'R',
#     'E' shifted by 'E' (position 4) becomes 'I',
#     'L' shifted by 'Y' (position 24) becomes 'J', and so on.
#     """

#     if request.method == "POST":
#         text = request.POST.get("text", "").strip()
#         key = request.POST.get("shift", "").strip()  # In Vigenère, the shift is a keyword
#         operation = request.POST.get("operation", "")
#         cipher = request.POST.get("cipher", "vigenere")

#         # Validate the key: must be alphabetic characters
#         if not key.isalpha():
#             return render(request, "ciphers/vigenere_cipher.html", {
#                 "error": "Key must only contain alphabetic characters.",
#                 "text": text,
#                 "shift": key,
#                 "cipher": cipher,
#                 "operation": operation,
#                 "vigenere_explanation": vigenere_explanation
#             })

#         if cipher == "vigenere":
#             if operation == "encrypt":
#                 result = vigenere_encrypt(text, key)
#                 opposite_result = vigenere_decrypt(result, key)
#                 operation_label = "Encryption"
#                 opposite_operation_label = "Decryption"
#                 data_label = f"Data to be decrypted: {result}"
#             elif operation == "decrypt":
#                 result = vigenere_decrypt(text, key)
#                 opposite_result = vigenere_encrypt(result, key)
#                 operation_label = "Decryption"
#                 opposite_operation_label = "Encryption"
#                 data_label = f"Data to be encrypted: {result}"

#         return render(request, "ciphers/vigenere_cipher.html", {
#             "text": text,
#             "shift": key,
#             "cipher": cipher,
#             "operation": operation,
#             "operation_label": operation_label,
#             "opposite_operation_label": opposite_operation_label,
#             "data_label": data_label,
#             "result": result,
#             "opposite_result": opposite_result,
#             "vigenere_explanation": vigenere_explanation
#         })

#     return render(request, "ciphers/vigenere_cipher.html", {
#         "vigenere_explanation": vigenere_explanation
#     })

# def vigenere_encrypt(text, key):
#     encrypted_text = []
#     key_length = len(key)
#     key_index = 0

#     for char in text:
#         if char.isalpha():
#             base = 65 if char.isupper() else 97
#             key_char = key[key_index % key_length].upper() if char.isupper() else key[key_index % key_length].lower()
#             shift = ord(key_char) - ord('A') if char.isupper() else ord(key_char) - ord('a')
#             encrypted_text.append(chr((ord(char) - base + shift) % 26 + base))
#             key_index += 1
#         else:
#             encrypted_text.append(char)

#     return ''.join(encrypted_text)

# def vigenere_decrypt(text, key):
#     decrypted_text = []
#     key_length = len(key)
#     key_index = 0

#     for char in text:
#         if char.isalpha():
#             base = 65 if char.isupper() else 97
#             key_char = key[key_index % key_length].upper() if char.isupper() else key[key_index % key_length].lower()
#             shift = ord(key_char) - ord('A') if char.isupper() else ord(key_char) - ord('a')
#             decrypted_text.append(chr((ord(char) - base - shift) % 26 + base))
#             key_index += 1
#         else:
#             decrypted_text.append(char)

#     return ''.join(decrypted_text)
from django.shortcuts import render

def vigenere_cipher(request):
    result = ""
    opposite_result = ""
    text = ""
    keyword = ""
    error = None
    opposite_operation_label = ""  # Default value for the opposite operation label
    data_label = ""  # Default value for the data label

    if request.method == 'POST':
        # Get the action, text, and keyword from the form
        action = request.POST.get('operation')
        text = request.POST.get('text', '')  # Retain the original case
        keyword = request.POST.get('keyword', '').upper()  # Still use uppercase for the keyword

        # Clean the input: remove non-alphabet characters, but retain spaces
        text = ''.join([ch for ch in text if ch.isalpha() or ch.isspace()])
        keyword = ''.join([ch for ch in keyword if ch.isalpha()])

        # Check if the action is encryption or decryption
        if action == 'encrypt':
            result = vigenere_encrypt(text, keyword)
            opposite_result = vigenere_decrypt(result, keyword)  # Calculate opposite (decryption)
            opposite_operation_label = "Decryption"
            data_label = "This is the decrypted result of the encrypted text."
        elif action == 'decrypt':
            result = vigenere_decrypt(text, keyword)
            opposite_result = vigenere_encrypt(result, keyword)  # Calculate opposite (encryption)
            opposite_operation_label = "Encryption"
            data_label = "This is the encrypted result of the decrypted text."
        else:
            error = "Invalid operation."

    return render(request, 'ciphers/vigenere_cipher.html', {
        'result': result,
        'opposite_result': opposite_result,
        'text': text,
        'keyword': keyword,
        'error': error,
        'opposite_operation_label': opposite_operation_label,
        'data_label': data_label
    })






def vigenere_encrypt(plaintext, keyword):
    ciphertext = []
    key_index = 0
    for i in range(len(plaintext)):
        p_char = plaintext[i]
        k_char = keyword[key_index % len(keyword)]
        
        # Handle uppercase and lowercase letters
        if p_char.isupper():
            shift = ord(k_char.upper()) - ord('A')  # Use uppercase for the key
            c_char = chr((ord(p_char) - ord('A') + shift) % 26 + ord('A'))
        elif p_char.islower():
            shift = ord(k_char.lower()) - ord('a')  # Use lowercase for the key
            c_char = chr((ord(p_char) - ord('a') + shift) % 26 + ord('a'))
        else:
            c_char = p_char  # Keep spaces or other characters unchanged
        
        ciphertext.append(c_char)
        key_index += 1
    return ''.join(ciphertext)

def vigenere_decrypt(ciphertext, keyword):
    plaintext = []
    key_index = 0
    for i in range(len(ciphertext)):
        c_char = ciphertext[i]
        k_char = keyword[key_index % len(keyword)]
        
        # Handle uppercase and lowercase letters
        if c_char.isupper():
            shift = ord(k_char.upper()) - ord('A')  # Use uppercase for the key
            p_char = chr((ord(c_char) - ord('A') - shift + 26) % 26 + ord('A'))
        elif c_char.islower():
            shift = ord(k_char.lower()) - ord('a')  # Use lowercase for the key
            p_char = chr((ord(c_char) - ord('a') - shift + 26) % 26 + ord('a'))
        else:
            p_char = c_char  # Keep spaces or other characters unchanged
        
        plaintext.append(p_char)
        key_index += 1
    return ''.join(plaintext)




#MARK: TEAM
def myTeam(request):
    return render(request, "ciphers/my_team.html")

#MARK: Home
def home(request):
    return render (request, "ciphers/home.html")