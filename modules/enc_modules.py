#code adapted from stackoverflow response, link below
#https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
#Martijn Pieters
#answered Mar 13, 2019 at 16:43 edited Apr 10 at 10:39
#sourced May 2022
#Fernet with password – key derived from password, weakens the security somewhat
#This approach was chosen for my SSS project so that the user would only need
#to remember their password rather than keeping the Fernet key, since these
#will be used to encrypt other text, that will then be stored as files
#which will make up the individual SSS shares 

import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.exceptions import InternalError as InternalError
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
iterations = 100_000

def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    try:
        key = _derive_key(password.encode(), salt, iterations)
    except InternalError:
        mywarnings.printwarningsInternalError()
        return
    return Fernet(key).decrypt(token)
