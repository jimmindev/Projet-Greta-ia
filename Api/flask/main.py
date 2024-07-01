from flask import Flask, request, jsonify
import mysql.connector
import jwt
import datetime
from functools import wraps

# pip install Flask mysql-connector-python jwt

app = Flask(__name__)

# Replace these values with your secret key and database connection details
SECRET_KEY = 'azerty123qsdfgh456'
db_config = {
    'host': '192.168.20.24',
    'user': 'jimmy',
    'password': 'jimmy',
    'database': 'Test_API'
}

data_user ={}

# Helper function to establish a database connection
def connect():
    return mysql.connector.connect(**db_config)

# Middleware to check and decode the token
def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(token)
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            # You can add additional checks here, such as validating user roles, etc.
            #print(data)
            #data_user[token] = data 
            #print(data_user)

            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.DecodeError as e:
            print(f"Error decoding token: {e}")
            return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            print(f"Unexpected error: {e}")
            return jsonify({'message': 'Unexpected error'}), 500
    return wrapper

# Select operation
@app.route('/select/<table>', methods=['GET'])
@token_required
def select(table):
    try:
        conn = connect()
        cursor = conn.cursor(dictionary=True)

        query = f"SELECT * FROM {table}"
        print(query)
        cursor.execute(query)
        rows = cursor.fetchall()

        return jsonify(rows)
    finally:
        cursor.close()
        conn.close()

# Insert operation
@app.route('/insert/<table>', methods=['POST'])
@token_required
def insert(table):
    try:
        conn = connect()
        cursor = conn.cursor()

        data = request.get_json()
        columns = ', '.join(data.keys())
        values = ', '.join([f"'{value}'" for value in data.values()])

        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        cursor.execute(query)

        conn.commit()

        return jsonify({'message': 'Insert successful'})
    finally:
        cursor.close()
        conn.close()

# Update operation
@app.route('/update/<table>/<id>', methods=['PUT'])
@token_required
def update(table, id):
    try:
        conn = connect()
        cursor = conn.cursor()

        data = request.get_json()
        set_clause = ', '.join([f"{key} = '{value}'" for key, value in data.items()])

        query = f"UPDATE {table} SET {set_clause} WHERE id = {id}"
        cursor.execute(query)

        conn.commit()

        return jsonify({'message': 'Update successful'})
    finally:
        cursor.close()
        conn.close()

# Delete operation
@app.route('/delete/<table>/<id>', methods=['DELETE'])
@token_required
def delete(table, id):
    try:
        conn = connect()
        cursor = conn.cursor()

        query = f"DELETE FROM {table} WHERE id = {id}"
        cursor.execute(query)

        conn.commit()

        return jsonify({'message': 'Delete successful'})
    finally:
        cursor.close()
        conn.close()

# Generate token 
@app.route('/get_token/<login>/<password>', methods=['GET'])
def generate_token2(login, password):
    try:
        conn = connect()
        cursor = conn.cursor()
        query = f"SELECT * FROM accounts where user = '{login}' and password = '{password}' "
        cursor.execute(query)
        user_data = cursor.fetchone()

        if user_data:
            # Assuming the order of columns in the table is (`id`, `user`, `password`, `expiration`, `roles`)
            expiration_date = user_data[3]  # Index 3 corresponds to the 'expiration' column

            # Convert expiration_date to datetime.datetime
            expiration_datetime = datetime.datetime.combine(expiration_date, datetime.time())
            #print(expiration_date)

            if user_data[4] == 1:  # Index 4 corresponds to the 'roles' column
                expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=1)
                expiration_datetime = datetime.datetime.combine(expiration_date, datetime.time())
                #print(expiration_datetime)

                # Ensure expiration_datetime is a Unix timestamp
                expiration_timestamp = int(expiration_datetime.timestamp())
                #print(expiration_date)


            token = jwt.encode({'login': login, 'role': user_data[4], 'exp': expiration_datetime}, SECRET_KEY, algorithm='HS256')

            return jsonify({'token': token})
        else:
            return jsonify({'error': 'Invalid login or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)