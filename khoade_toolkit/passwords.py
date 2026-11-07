"""Gerador de senhas aleatórias usando o módulo secrets."""

import secrets
import string

SYMBOLS = "!@#$%^&*()-_=+"
MIN_LENGTH = 8


def generate_password(length=16, symbols=True):
    """Gera uma senha com pelo menos um caractere de cada grupo usado."""
    if length < MIN_LENGTH:
        raise ValueError(f"o tamanho mínimo é {MIN_LENGTH}")
    pools = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if symbols:
        pools.append(SYMBOLS)
    alphabet = "".join(pools)
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if all(any(char in pool for char in password) for pool in pools):
            return password
