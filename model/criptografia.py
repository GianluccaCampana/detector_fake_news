#criptografia
import hashlib


def criptografar(senha):
    return hashlib.md5(senha.encode()).hexdigest()