import jwt
import datetime

# Secret key for encoding and decoding the token
SECRET_KEY = 'azerty123qsdfgh456'

# Payload (information you want to include in the token)
payload = {
    'user_id': 1,
    'username': 'jimmy',
    'exp': datetime.datetime.now() + datetime.timedelta(days=1)  # Token expiration time
}

# Encode the token
token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

print(f'Token: {token}')