from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64



with open("private.key", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )

with open("enc.bin", "rb") as f:
    ciphertext = base64.b64decode(f.read())
    print(len(ciphertext))

plaintext = private_key.decrypt(
    ciphertext,
    padding.PKCS1v15()
)
print(plaintext)
