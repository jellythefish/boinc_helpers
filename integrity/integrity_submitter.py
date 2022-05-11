#!/usr/bin/env python3

# Run this script from root project!

import argparse
import hashlib
from pathlib import Path
import logging
import subprocess
from random import randint
import time
import os

MAX_INT = 10 ** 9

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


def process_input(input_files):
    hashes = calculate_file_hashes(input_files)
    merkle_root = calculate_merkle_root(hashes)
    ts = int(time.time())
    rand_num = randint(0, MAX_INT)
    filename = "MERKLE_ROOT_{}_{}".format(ts, rand_num)
    with open(filename, "w") as f:
        f.write(merkle_root)
    return filename


def modify_xml(app_name, merkle_root_filename):
    folder = "templates"
    filename = "{}_in".format(app_name)
    filepath = "{}/{}".format(folder, filename)
    with open(filepath, "r") as f:
        wu_template_content = f.read()
    content_list = wu_template_content.split("<workunit>")
    insert = """
    <file_info>
        <no_delete/>
    </file_info>
    <workunit>
        <file_ref>
            <open_name>{}</open_name>
            <copy_file/>
        </file_ref>
    """.format(merkle_root_filename)
    content_list.insert(1, insert)
    wu_template_modified = "{}_modified".format(filename)
    new_path = "{}/{}".format(folder, wu_template_modified)
    with open(new_path, "w") as f:
        f.write("".join(content_list))
    return new_path


def stage_in(file, copy=False):
    logging.debug("Stagging in {}".format(file))
    args = [
        "bin/stage_file",
    ]
    if copy:
        args.append("--copy")
    args.append(file)
    out = subprocess.check_output(args)
    logging.debug(out)


def submit_job(appname, wu_template_path, input_files):
    logging.debug("Generating workunit for app {}".format(appname))
    args = [
        "bin/create_work",
        "--appname",
        appname,
        "--wu_template",
        wu_template_path,
        "--verbose"
    ]
    for file in input_files:
        filepath = Path(file)
        args.append(filepath.name)
    out = subprocess.check_output(args)
    logging.debug(out)


def clean_up(wu_template_path):
    os.remove(wu_template_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", required=True, help="application name", type=str)
    parser.add_argument("--input", required=True, help="path to input files for wu", nargs='+')
    args = parser.parse_args()
    merkle_root_filename = process_input(args.input)
    wu_template_path = modify_xml(args.app, merkle_root_filename)
    stage_in(merkle_root_filename)
    for file in args.input:
        stage_in(file, copy=True)
    all_input_files = [merkle_root_filename, *args.input]
    submit_job(args.app, wu_template_path, all_input_files)
    clean_up(wu_template_path)
