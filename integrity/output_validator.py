#!/usr/bin/env python3

import hashlib
from sys import exit
from sys import argv
from pathlib import Path
import logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


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
    logging.info(str(argv))

    wu_id = argv[-1]
    files = argv[1:-1]
    output_files = []
    for file in files:
        if file.endswith("_output_hash"):
            output_hash_client_filepath = file
        elif file.endswith("_output_submitter_out"):
            continue
        else:
            output_files.append(file)

    try:
        hashes = calculate_file_hashes(output_files)
        merkle_root = calculate_merkle_root(hashes)
        concatenated = merkle_root + wu_id
        output_hash_server = hashlib.sha256(concatenated.encode("utf-8")).hexdigest()
    except Exception as e:
        logging.error("Failed to calculate input hash on client-side: {}".format(e))
        exit(1)

    try:
        with open(output_hash_client_filepath, "r") as f:
            output_hash_client = f.read()
        assert output_hash_server == output_hash_client, "integrity hashes are not equal foroutput files"
    except Exception as e:
        logging.error("Integrity output validation has failed: {}".format(e))
        exit(1)

    logging.info(
        "Validation has successfully passed: server integrity output hash"
        "\n{}\nequals to client integrity output hash\n{}".format(
        output_hash_server, output_hash_client
    ))


if __name__ == "__main__":
    main()