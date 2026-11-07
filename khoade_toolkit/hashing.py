"""Cálculo de hash de arquivos."""

import hashlib

ALGORITHMS = ("md5", "sha1", "sha256", "sha512")


def hash_file(path, algorithm="sha256", chunk_size=1024 * 1024):
    """Retorna o hash hexadecimal do arquivo, lendo em blocos."""
    if algorithm not in ALGORITHMS:
        raise ValueError(f"algoritmo não suportado: {algorithm}")
    digest = hashlib.new(algorithm)
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()
