#!/usr/bin/env python

import sys

import MySQLdb

# TODO: later to use config
config = {
    "db": "gtcl",
    "host": "localhost",
    "port": 3306,
    "user": "",
    "password": ""
}

def main():
    if "--error" in sys.argv:
        print("Error occured while assimilating result, args: ", sys.argv)
        return
    wu_id = sys.argv[1]
    files = sys.argv[1:]

    try:
        db_connection= MySQLdb.connect(config["host"], config["user"], config["password"], config["db"])
    except Exception as e:
        print("Can't connect to database ", e)
 
    cursor = db_connection.cursor()
    query = 'SELECT * FROM result WHERE workunitid={};'.format(wu_id)
    cursor.execute(query)
    m = cursor.fetchall()
    column_names = [elem[0] for elem in cursor.description]
    values = dict()
    assert len(column_names) == len(m[0])
    for i in range(len(column_names)):
        values[column_names[i]] = m[0][i]
    
    host_id = values["hostid"]
    for file in files:
        if file.endswith("pubkey"):
            pubkey_path = file
            break
    with open(pubkey_path, "rb") as f:
        pubkey_content = f.read()
    query= "UPDATE host SET public_key=%s WHERE id=%s"
    cursor.execute(query, (pubkey_content, host_id))
    m = cursor.fetchall()
    db_connection.commit()
    db_connection.close()

    integrity_path = pubkey_path.split("upload")[0] + "integrity/"
    generation_success_file = integrity_path + "GEN_KEYS_SUCCESS_HOST_1"
    with open(generation_success_file, "w") as f:
        f.write("")


if __name__ == "__main__":
    main()
