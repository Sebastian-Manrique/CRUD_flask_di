import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def add_padding(base64_string):
    return base64_string + '=' * (-len(base64_string) % 4)


def decrypt_data(encrypted_data, key):
    # Ajusta el padding de la cadena base64
    encrypted_data = add_padding(encrypted_data)
    # Decodifica los datos cifrados de base64
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]  # Inicialización del vector
    encrypted_data = encrypted_data[16:]

    # Configura el cifrador AES en modo CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Elimina el padding
    pad = decrypted_data[-1]
    decrypted_data = decrypted_data[:-pad]

    return decrypted_data.decode('utf-8')


# Prueba con datos ficticios
encrypted_contra = "EncryptedStringHere"
secret_key = b'Secret Passphrase'
try:
    contra = decrypt_data(encrypted_contra, secret_key)
    print(f"Contraseña desencriptada: {contra}")
except Exception as e:
    print(f"Error al desencriptar los datos: {e}")
