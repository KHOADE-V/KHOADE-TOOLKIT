"""Renomeia arquivos de uma pasta em lote com prefixo e numeração."""

from pathlib import Path


def plan_rename(directory, prefix, start=1, width=3):
    """Planeja a renomeação: retorna uma lista de pares (origem, destino)."""
    directory = Path(directory)
    if not directory.is_dir():
        raise NotADirectoryError(str(directory))
    files = [
        item for item in sorted(directory.iterdir())
        if item.is_file() and not item.name.startswith(".")
    ]
    plan = []
    for offset, source in enumerate(files):
        number = f"{start + offset:0{width}d}"
        plan.append((source, source.with_name(f"{prefix}{number}{source.suffix.lower()}")))
    return plan


def apply_plan(plan):
    """Executa o plano em duas fases para evitar colisões entre nomes."""
    sources = {source for source, _ in plan}
    for source, destination in plan:
        if source != destination and destination.exists() and destination not in sources:
            raise FileExistsError(str(destination))
    temporaries = []
    for source, destination in plan:
        if source == destination:
            continue
        temporary = source.with_name(f".khoade-tmp-{source.name}")
        source.rename(temporary)
        temporaries.append((temporary, destination))
    for temporary, destination in temporaries:
        temporary.rename(destination)
