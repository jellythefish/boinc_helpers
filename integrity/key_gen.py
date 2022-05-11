from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from pathlib import Path
import argparse
import traceback


def main(path):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    path = Path(path)
    with open(path / "private.key", 'wb') as content_file:
        content_file.write(pem_private)
    with open(path / "public.key", 'wb') as content_file:
        content_file.write(pem_public)
    


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--path", required=True, help="path to save keys to", type=str)
        args = parser.parse_args()
        main(args.path)
    except Exception as e:
        with open("stderr", "w") as f:
            tb_str = ''.join(traceback.format_exception(None, e, e.__traceback__))
            f.write(tb_str)
