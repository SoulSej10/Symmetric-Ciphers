from django.shortcuts import render
from .models import CaesarCipherData
from .utils import caesar_encrypt, caesar_decrypt
from django.http import JsonResponse

# Create your views here.

# def caesar_cipher_view(request):
#     result = None
#     opposite_result = None
#     steps = []

#     if request.method == "POST":
#         text = request.POST.get("text")
#         shift = int(request.POST.get("shift", 0))
#         operation = request.POST.get("operation")
#         cipher = request.POST.get("cipher", "caesar")
        
#         if cipher == "caesar":
#             if operation == "encrypt":
#                 result, steps = caesar_encrypt_with_steps(text, shift)
#                 opposite_result, opposite_steps = caesar_decrypt_with_steps(result, shift)
#             elif operation == "decrypt":
#                 result, steps = caesar_decrypt_with_steps(text, shift)
#                 opposite_result, opposite_steps = caesar_encrypt_with_steps(result, shift)

#         return render(request, "ciphers/caesar_cipher.html", {
#             "text": text,
#             "shift": shift,
#             "cipher": cipher,
#             "operation": operation,
#             "result": result,
#             "opposite_result": opposite_result,
#             "steps": steps  # Passing steps to the template
#         })

#     return render(request, "ciphers/caesar_cipher.html")
def caesar_cipher_view(request):
    result = None
    opposite_result = None
    steps = []
    opposite_steps = []
    operation_label = None
    opposite_operation_label = None
    data_label = None

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
                "operation": operation
            })
        
        shift = int(shift_raw)

        if cipher == "caesar":
            if operation == "encrypt":
                result, steps = caesar_encrypt_with_steps(text, shift)
                opposite_result, opposite_steps = caesar_decrypt_with_steps(result, shift)
                operation_label = "Encryption"
                opposite_operation_label = "Decryption"
                data_label = f"Data to be decrypted: {result}"
            elif operation == "decrypt":
                result, steps = caesar_decrypt_with_steps(text, shift)
                opposite_result, opposite_steps = caesar_encrypt_with_steps(result, shift)
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
            "steps": steps,
            "opposite_steps": opposite_steps
        })

    return render(request, "ciphers/caesar_cipher.html")



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




# New view to update the opposite result dynamically via AJAX
# def update_opposite_result(request):
#     if request.method == "POST":
#         import json
#         data = json.loads(request.body)
#         cipher = data.get("cipher")
#         operation = data.get("operation")

#         # Example text and shift for demo
#         text = "Your Example Text"
#         shift = 3  # Example shift value

#         steps = []
#         opposite_result = ""
        
#         if cipher == "caesar":
#             if operation == "encrypt":
#                 opposite_result, steps = caesar_decrypt_with_steps(text, shift)  # Decrypting instead of encrypting
#             elif operation == "decrypt":
#                 opposite_result, steps = caesar_encrypt_with_steps(text, shift)  # Encrypting instead of decrypting

#         return JsonResponse({"result": opposite_result, "steps": steps})

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
