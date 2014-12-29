from binascii import hexlify
from hashlib import pbkdf2_hmac
from repo.settings.settings import settings

secret = settings['cookie_secret']


def hash_password(password):
    return hexlify(pbkdf2_hmac('sha256', password, secret, 100000))


def check_password(password, hashed):
    return hashed == hash_password(password)