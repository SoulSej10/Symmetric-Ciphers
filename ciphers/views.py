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

from django.shortcuts import render

def vigenere_cipher(request):
    result = ""
    opposite_result = ""
    text = ""
    keyword = ""
    error = None
    opposite_operation_label = ""
    data_label = ""
    cipher_grid = []  # To hold the cipher grid for encryption/decryption
    operation_label = ""  # To describe the operation performed

    if request.method == 'POST':
        action = request.POST.get('operation')
        text = request.POST.get('text', '')
        keyword = request.POST.get('keyword', '').upper()

        # Clean input
        text = ''.join([ch for ch in text if ch.isalpha() or ch.isspace()])
        keyword = ''.join([ch for ch in keyword if ch.isalpha()])

        if not keyword:
            error = "Keyword must only contain alphabetic characters."
        elif action == 'encrypt':
            result, cipher_grid = vigenere_encrypt_with_grid(text, keyword)
            opposite_result, _ = vigenere_decrypt_with_grid(result, keyword)
            opposite_operation_label = "Decryption"
            data_label = "This is the decrypted result of the encrypted text."
            operation_label = "Encryption Process"
        elif action == 'decrypt':
            result, cipher_grid = vigenere_decrypt_with_grid(text, keyword)
            opposite_result, _ = vigenere_encrypt_with_grid(result, keyword)
            opposite_operation_label = "Encryption"
            data_label = "This is the encrypted result of the decrypted text."
            operation_label = "Decryption Process"
        else:
            error = "Invalid operation."

    return render(request, 'ciphers/vigenere_cipher.html', {
        'result': result,
        'opposite_result': opposite_result,
        'text': text,
        'keyword': keyword,
        'error': error,
        'opposite_operation_label': opposite_operation_label,
        'data_label': data_label,
        'cipher_grid': cipher_grid,
        'operation_label': operation_label,
    })

def vigenere_encrypt_with_grid(plaintext, keyword):
    ciphertext = []
    cipher_grid = []
    key_index = 0

    for i in range(len(plaintext)):
        p_char = plaintext[i]
        if p_char.isalpha():
            k_char = keyword[key_index % len(keyword)]
            shift = ord(k_char.upper()) - ord('A')
            if p_char.isupper():
                c_char = chr((ord(p_char) - ord('A') + shift) % 26 + ord('A'))
            else:
                c_char = chr((ord(p_char) - ord('a') + shift) % 26 + ord('a'))

            # Add to cipher grid
            cipher_grid.append((p_char, k_char, shift, c_char))
            key_index += 1
        else:
            c_char = p_char
            cipher_grid.append((p_char, '-', '-', c_char))

        ciphertext.append(c_char)
    return ''.join(ciphertext), cipher_grid


def vigenere_decrypt_with_grid(ciphertext, keyword):
    plaintext = []
    cipher_grid = []
    key_index = 0

    for i in range(len(ciphertext)):
        c_char = ciphertext[i]
        if c_char.isalpha():
            k_char = keyword[key_index % len(keyword)]
            shift = ord(k_char.upper()) - ord('A')
            if c_char.isupper():
                p_char = chr((ord(c_char) - ord('A') - shift + 26) % 26 + ord('A'))
            else:
                p_char = chr((ord(c_char) - ord('a') - shift + 26) % 26 + ord('a'))

            # Add to cipher grid
            cipher_grid.append((c_char, k_char, shift, p_char))
            key_index += 1
        else:
            p_char = c_char
            cipher_grid.append((c_char, '-', '-', p_char))

        plaintext.append(p_char)
    return ''.join(plaintext), cipher_grid



#MARK: Playfair
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.utils.html import escape


# Function to generate Playfair matrix
def generate_playfair_matrix(key):
    matrix = []
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 'J' is excluded
    used = set()

    # Clean up the key and add unique characters
    key = ''.join([char.upper() for char in key if char.isalpha()])
    for char in key:
        if char not in used:
            used.add(char)
            matrix.append(char)

    # Fill the matrix with the remaining characters from the alphabet
    for char in alphabet:
        if char not in used:
            used.add(char)
            matrix.append(char)

    return matrix

# Function to create digraphs from text
def create_digraphs(text):
    text = ''.join([char.upper() for char in text if char.isalpha()]).replace('J', 'I')
    digraphs = []

    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i] == text[i + 1]:
            digraphs.append(text[i] + 'X')
            i += 1
        else:
            digraphs.append(text[i] + (text[i + 1] if i + 1 < len(text) else 'X'))
            i += 2

    return digraphs

# Function to find position of character in matrix
def find_position(matrix, char):
    index = matrix.index(char)
    return index // 5, index % 5

# Encryption function
def encrypt_playfair(key, text):
    matrix = generate_playfair_matrix(key)
    digraphs = create_digraphs(text)
    encrypted_text = ''
    process = []

    for pair in digraphs:
        first, second = pair
        pos1 = find_position(matrix, first)
        pos2 = find_position(matrix, second)

        if pos1[0] == pos2[0]:
            new_first = matrix[pos1[0] * 5 + (pos1[1] + 1) % 5]
            new_second = matrix[pos2[0] * 5 + (pos2[1] + 1) % 5]
            rule = "Same row"
        elif pos1[1] == pos2[1]:
            new_first = matrix[((pos1[0] + 1) % 5) * 5 + pos1[1]]
            new_second = matrix[((pos2[0] + 1) % 5) * 5 + pos2[1]]
            rule = "Same column"
        else:
            new_first = matrix[pos1[0] * 5 + pos2[1]]
            new_second = matrix[pos2[0] * 5 + pos1[1]]
            rule = "Rectangle"

        encrypted_text += new_first + new_second
        process.append({
            'pair': f"{first}{second}",
            'rule': rule,
            'result': f"{new_first}{new_second}"
        })

    return encrypted_text, process

# Decryption function
# Decryption function with logic to clean 'X' from added values
def decrypt_playfair(key, text):
    matrix = generate_playfair_matrix(key)
    digraphs = create_digraphs(text)
    decrypted_text = ''

    for pair in digraphs:
        first, second = pair
        pos1 = find_position(matrix, first)
        pos2 = find_position(matrix, second)

        if pos1[0] == pos2[0]:
            decrypted_text += matrix[pos1[0] * 5 + (pos1[1] - 1) % 5]
            decrypted_text += matrix[pos2[0] * 5 + (pos2[1] - 1) % 5]
        elif pos1[1] == pos2[1]:
            decrypted_text += matrix[((pos1[0] - 1) % 5) * 5 + pos1[1]]
            decrypted_text += matrix[((pos2[0] - 1) % 5) * 5 + pos2[1]]
        else:
            decrypted_text += matrix[pos1[0] * 5 + pos2[1]]
            decrypted_text += matrix[pos2[0] * 5 + pos1[1]]

    # Clean the decrypted_text by removing artifacts like trailing 'X'
    # Logic to undo inserted 'X' during encryption
    cleaned_text = ''
    i = 0
    while i < len(decrypted_text):
        # Case: Handle double repeated letters replaced with X
        if i + 1 < len(decrypted_text) and decrypted_text[i] == decrypted_text[i + 1]:
            cleaned_text += decrypted_text[i]
            i += 2
        elif decrypted_text[i] == 'X' and (i == len(decrypted_text) - 1 or decrypted_text[i - 1] == decrypted_text[i - 1]):
            # Handle if X is at end or corresponds to padding
            i += 1
        else:
            cleaned_text += decrypted_text[i]
            i += 1

    return cleaned_text

# View for Playfair Cipher
def playfair_cipher(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            key = data.get('key', '').strip()
            text = data.get('text', '').strip()
            operation = data.get('operation', 'encrypt')
        else:
            key = request.POST.get('key', '').strip()
            text = request.POST.get('text', '').strip()
            operation = request.POST.get('operation', 'encrypt')

        if operation == 'encrypt':
            result, process = encrypt_playfair(key, text)
        else:
            result = decrypt_playfair(key, text)
            process = []  # We're not showing the process for decryption

        return JsonResponse({'result': result, 'process': process})

    return render(request, 'ciphers/playfair_cipher.html')


#MARK: Single Columnar
# views.py

from django.shortcuts import render
from django.http import JsonResponse

def columnar_cipher(request):
    message = ''
    key = ''
    encrypted_message = ''
    decrypted_message = ''
    cipher_grid = []
    order = []

    if request.method == 'POST':
        action = request.POST.get('action', '')
        message = request.POST.get('message', '')
        key = request.POST.get('key', '').upper()

        if action == 'encrypt':
            # Primary: Encrypt the message
            encrypted_message, cipher_grid, order = encrypt(message, key)
            # Secondary: Decrypt the newly encrypted message
            decrypted_message = decrypt(encrypted_message, key)
        elif action == 'decrypt':
            # Primary: Decrypt the message
            decrypted_message = decrypt(message, key)
            # Secondary: Encrypt the newly decrypted message
            encrypted_message, cipher_grid, order = encrypt(decrypted_message, key)

    return render(request, 'ciphers/singleColumnar_cipher.html', {
        'message': message,
        'key': key,
        'encrypted_message': encrypted_message,
        'decrypted_message': decrypted_message,
        'cipher_grid': cipher_grid,
        'order': order
    })


def encrypt(message, key):
    # Clean the message by removing spaces and converting to uppercase
    clean_message = message.upper().replace(' ', '_')  # Replace spaces with underscores

    # Calculate how many padding characters we need
    num_cols = len(key)
    padded_message = clean_message

    # If the message isn't a multiple of the key length, pad the message in between words
    if len(padded_message) % num_cols != 0:
        padded_message += '_' * (num_cols - len(padded_message) % num_cols)

    # Create the grid by splitting the message into rows
    grid = [list(padded_message[i:i + num_cols]) for i in range(0, len(padded_message), num_cols)]

    # Create the order based on the alphabetical sorting of the key
    order = sorted(range(len(key)), key=lambda k: key[k])

    # Read the grid column by column in the sorted order of the key
    encrypted = ''.join(''.join(row[i] for row in grid) for i in order)

    return encrypted, grid, [i + 1 for i in order]  # Return the order for display


def decrypt(encrypted_message, key):
    # Determine the number of rows and columns based on the encrypted message length
    message_length = len(encrypted_message)
    num_cols = len(key)
    num_rows = (message_length + num_cols - 1) // num_cols  # ceil(message_length / num_cols)

    # Create an empty grid to fill
    grid = [[''] * num_cols for _ in range(num_rows)]

    # Create the order based on the alphabetical sorting of the key
    order = sorted(range(len(key)), key=lambda k: key[k])

    # Fill the grid column by column in the order defined by the key
    index = 0
    for col in order:
        for row in range(num_rows):
            if index < message_length:
                grid[row][col] = encrypted_message[index]
                index += 1

    # Read the grid row by row to reconstruct the decrypted message
    decrypted = ''.join(''.join(row) for row in grid).rstrip('_').replace('_', ' ')  # Clean up padding
    return decrypted



#MARK: Double Columnar
from django.shortcuts import render


def double_columnar_cipher(request):
   return render(request, "ciphers/double_columnar_cipher.html")



#MARK: TEAM
def myTeam(request):
    return render(request, "ciphers/my_team.html")

#MARK: Home
def home(request):
    return render (request, "ciphers/home.html")