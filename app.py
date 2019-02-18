from flask import Flask, abort, jsonify, request
import hashlib
import json
import os
import sqlite3

app = Flask(__name__)


def md5(json_obj):
    json_copy = json_obj.copy()
    del json_copy['md5checksum']
    json_b = json.dumps(json_copy, sort_keys=False).encode()
    checksum = hashlib.md5(json_b).hexdigest()
    return checksum


def compare_checksum(json_obj):
    return md5(json_obj) == json_obj['md5checksum']


def create_db(db_filename, schema_filename):
    if not os.path.exists(db_filename):
        with sqlite3.connect(db_filename) as conn:
            print('Creating schema')
            schema_script = """
                create table users1 (
                user_id text,
                name text,
                date date,
                hw text,
                md5checksum text
                );"""
            with open(schema_filename, 'w') as f:
                f.write(schema_script)
            conn.execute(schema_script)


def write_to_db(doc, db_filename):
    with sqlite3.connect(db_filename) as conn:
        print('Writing data')
        conn.execute("""
        insert into users1 (user_id, name, date, hw, md5checksum)
        values (?,?,?,?,?)""", (doc['user_id'], doc['name'], doc['date'], doc['hw'], doc['md5checksum']))


def read_from_db(user_id, db_filename):
    with sqlite3.connect(db_filename) as conn:
        print('Reading data')
        data = conn.execute("""
        select * from users1
        where user_id=?""", user_id).fetchall()
        result = []
        for row in data:
            result.append(dict(zip(("user_id", "name", "date", "hw", "md5checksum"), row)))
        return result


create_db('users_db.db', 'schema.sql')


@app.route('/user', methods=['POST'])
def first_endpoint():
    if not request.json:
        abort(400)
    else:
        for doc in request.json:
            if compare_checksum(doc):
                write_to_db(doc, 'users_db.db')
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/user/<user_id>', methods=['GET'])
def second_endpoint(user_id):
    return jsonify(read_from_db(user_id, 'users_db.db'))


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True, use_reloader=False)
