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
    """
    Generates a salted hash of the password

    :param plain_text_password: the input password
    :return: bytes
    """
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    """
    Checks whether the hashed password comes from this password. Using bcrypt, the salt is saved into the hash itself

    :param plain_text_password: the password from the input
    :param hashed_password: the salted hash from the datastore
    :return: boolean
    """
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)
