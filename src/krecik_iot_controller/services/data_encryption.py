import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def encrypt_aes256(
    key: str,
    iv: str,
    message: str,
) -> str:
    cipher = Cipher(
        algorithms.AES256(bytes.fromhex(key)),
        modes.CFB(bytes.fromhex(iv)),
        backend=default_backend(),
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(
        message.encode('utf-8')) + encryptor.finalize()
    return iv + ciphertext.hex()
