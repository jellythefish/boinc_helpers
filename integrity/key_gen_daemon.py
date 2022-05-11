#!/usr/bin/env python3

import time
from pathlib import Path
import subprocess
import logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


submitted_hosts = set()

def submit_genkey_workunit(host_id):
    logging.debug("Generating workunit for host id {}".format(host_id))
    out = subprocess.check_output([
        "bin/create_work",
        "--appname",
        "key_gen",
        "--target_host",
        host_id,
        "--verbose"
    ], cwd="..")
    logging.debug(out)


def main():
    logging.info("Running Key Generator Daemon")
    while True:
        integrity_dir = Path("../integrity")
        for file in sorted(integrity_dir.iterdir()):
            if file.name.startswith("GEN_KEYS_HOST_ID_"):
                host_id = file.name.split("_")[-1]
                if host_id not in submitted_hosts:
                    submit_genkey_workunit(host_id)
                    submitted_hosts.add(host_id)
            elif file.name.startswith("GEN_KEYS_SUCCESS_HOST_"):
                host_id = file.name.split("_")[-1]
                logging.debug("successfully generated keys for host {}".format(host_id))
                submitted_hosts.remove(host_id)
                filename = "GEN_KEYS_HOST_ID_" + host_id
                file_to_delete = integrity_dir / filename
                file_to_delete.unlink()
                file.unlink()
        time.sleep(5)


if __name__ == "__main__":
    main()
