import bcrypt
from nacl.exceptions import CryptoError

from nacl.secret import SecretBox

from Crypto.Protocol.KDF import scrypt


def encrypt(message, shared_key):
    key = scrypt(shared_key, 0, 32, N=2 ** 14, r=8, p=1)
    box = SecretBox(key)
    return box.encrypt(message.encode('utf-8'))


def decrypt(message, shared_key):
    # deriviation function to extract a key from password
    key = scrypt(shared_key, 0, 32, N=2 ** 14, r=8, p=1)
    box = SecretBox(key)
    try:
        plaintext = box.decrypt(message)
    except CryptoError as exc:
        print(exc)
        return None
    return plaintext.decode('utf-8')


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


# def hash_password(password, maxtime=0.5, datalength=64):
#     return sc.encrypt(os.urandom(datalength), password, maxtime=maxtime)
#
# def verify_password(hashed_password, guessed_password, maxtime=0.5):
#     try:
#         sc.decrypt(hashed_password, guessed_password, maxtime)
#         return True
#     except sc.error:
#         return False
