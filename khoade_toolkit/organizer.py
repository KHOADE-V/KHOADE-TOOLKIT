"""Organiza os arquivos de uma pasta em subpastas por tipo."""

import shutil
from pathlib import Path

CATEGORIES = {
    "Imagens": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".heic"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".ogg", ".m4a"},
    "Documentos": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf"},
    "Planilhas": {".xls", ".xlsx", ".csv", ".ods"},
    "Apresentacoes": {".ppt", ".pptx", ".odp"},
    "Compactados": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Codigo": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp",
               ".go", ".rs", ".sh", ".json"},
    "Instaladores": {".exe", ".msi", ".apk", ".deb", ".dmg"},
}
OTHER = "Outros"


def category_for(path):
    """Retorna o nome da categoria de um arquivo pela extensão."""
    extension = Path(path).suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return OTHER


def _free_name(destination):
    """Evita sobrescrever: acrescenta ' (1)', ' (2)'... se o nome já existir."""
    if not destination.exists():
        return destination
    number = 1
    while True:
        candidate = destination.with_name(
            f"{destination.stem} ({number}){destination.suffix}"
        )
        if not candidate.exists():
            return candidate
        number += 1


def organize(directory, apply=False):
    """Planeja (e opcionalmente executa) a organização da pasta.

    Só considera arquivos do primeiro nível e ignora arquivos ocultos.
    Retorna uma lista de pares (origem, destino).
    """
    directory = Path(directory)
    if not directory.is_dir():
        raise NotADirectoryError(str(directory))
    moves = []
    for item in sorted(directory.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        destination = _free_name(directory / category_for(item) / item.name)
        moves.append((item, destination))
        if apply:
            destination.parent.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
    return moves
