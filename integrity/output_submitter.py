from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import hashlib
from pathlib import Path
import logging
from sys import exit
import argparse

logging.basicConfig(filename="output_submitter.log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

ENC_FILENAME = "enc.bin"
PRIVATE_KEY_FILEPATH = Path("../../projects/178.154.210.253_gtcl/private.key")


def decrypt_enc_file():
    with open(PRIVATE_KEY_FILEPATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    with open(ENC_FILENAME, "rb") as f:
        ciphertext = base64.b64decode(f.read())


    plaintext = private_key.decrypt(
        ciphertext,
        padding.PKCS1v15()
    )
    return plaintext.decode('utf-8')


def calculate_file_hashes(input_files):
    hashes = []
    for file_path in input_files:
        with open(Path(file_path), "rb") as f:
            content = f.read()
            hashes.append(hashlib.sha256(content).hexdigest())
    hashes = sorted(hashes)
    return hashes


def combine_hashes(hash_one, hash_two):
    concatenated = hash_one + hash_two
    return hashlib.sha256(concatenated.encode("utf-8")).hexdigest()


def calculate_merkle_root(hashes):
    if len(hashes) == 1:
        return hashes[0]
    new_hashes = []
    for i in range(0, len(hashes) - 1, 2):
        new_hashes.append(combine_hashes(hashes[i], hashes[i + 1]))
     # if odd, hash last item twice
    if len(hashes) % 2 == 1:
        new_hashes.append(combine_hashes(hashes[-1], hashes[-1]))
    return calculate_merkle_root(new_hashes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="path to output files to server", nargs='+')
    args = parser.parse_args()

    try:
        decrypted = decrypt_enc_file()
    except Exception as e:
        logging.error("Failed to decrypt secret from server: {}".format(e))
        exit(1)

    try:
        logging.info("output_files: {}".format(args.output))
        hashes = calculate_file_hashes(args.output)
        logging.info("hashes: {}".format(hashes))
        merkle_root = calculate_merkle_root(hashes)
        logging.info("merkle_root: {}".format(merkle_root))
        concatenated = merkle_root + decrypted
        logging.info("concatenated: {}".format(concatenated))
        output_hash_client = hashlib.sha256(concatenated.encode("utf-8")).hexdigest()
        logging.info("output_hash_client: {}".format(output_hash_client))
    except Exception as e:
        logging.error("Failed to calculate input hash on client-side: {}".format(e))
        exit(1)

    try:
        with open("output_hash", "w") as f:
            f.write(output_hash_client)
    except Exception as e:
        logging.error("Failed to write integrity output hash to file: {}".format(e))
        exit(1)


if __name__ == '__main__':
    main()
