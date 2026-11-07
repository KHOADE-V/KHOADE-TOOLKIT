"""Interface de linha de comando do KHOADE Toolkit."""

import argparse
import sys
from pathlib import Path

from . import __version__
from .hashing import ALGORITHMS, hash_file
from .organizer import organize
from .passwords import generate_password
from .renamer import apply_plan, plan_rename


def _cmd_hash(args):
    status = 0
    for name in args.arquivos:
        try:
            digest = hash_file(name, args.algoritmo)
        except OSError as error:
            print(f"erro: {name}: {error.strerror or error}", file=sys.stderr)
            status = 1
            continue
        print(f"{digest}  {name}")
    return status


def _cmd_senha(args):
    for _ in range(args.quantidade):
        print(generate_password(args.tamanho, symbols=not args.sem_simbolos))
    return 0


def _print_moves(moves, apply):
    for source, destination in moves:
        print(f"{source.name} -> {destination.parent.name}/{destination.name}")
    if not moves:
        print("nada para fazer")
    elif not apply:
        print(f"\n(simulação) {len(moves)} arquivo(s). Use --aplicar para executar.")
    else:
        print(f"\n{len(moves)} arquivo(s) movido(s).")


def _cmd_organizar(args):
    moves = organize(Path(args.pasta), apply=args.aplicar)
    _print_moves(moves, args.aplicar)
    return 0


def _cmd_renomear(args):
    plan = plan_rename(Path(args.pasta), args.prefixo, args.inicio, args.largura)
    for source, destination in plan:
        print(f"{source.name} -> {destination.name}")
    if not plan:
        print("nada para fazer")
        return 0
    if args.aplicar:
        apply_plan(plan)
        print(f"\n{len(plan)} arquivo(s) renomeado(s).")
    else:
        print(f"\n(simulação) {len(plan)} arquivo(s). Use --aplicar para executar.")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="khoade", description="Utilitários de linha de comando do dia a dia."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_hash = sub.add_parser("hash", help="calcula o hash de arquivos")
    p_hash.add_argument("arquivos", nargs="+")
    p_hash.add_argument("-a", "--algoritmo", choices=ALGORITHMS, default="sha256")
    p_hash.set_defaults(func=_cmd_hash)

    p_senha = sub.add_parser("senha", help="gera senhas aleatórias")
    p_senha.add_argument("-t", "--tamanho", type=int, default=16)
    p_senha.add_argument("-n", "--quantidade", type=int, default=1)
    p_senha.add_argument("--sem-simbolos", action="store_true")
    p_senha.set_defaults(func=_cmd_senha)

    p_org = sub.add_parser("organizar", help="separa os arquivos de uma pasta por tipo")
    p_org.add_argument("pasta")
    p_org.add_argument("--aplicar", action="store_true", help="executa de verdade")
    p_org.set_defaults(func=_cmd_organizar)

    p_ren = sub.add_parser("renomear", help="renomeia arquivos em lote com numeração")
    p_ren.add_argument("pasta")
    p_ren.add_argument("-p", "--prefixo", required=True)
    p_ren.add_argument("-i", "--inicio", type=int, default=1)
    p_ren.add_argument("-w", "--largura", type=int, default=3)
    p_ren.add_argument("--aplicar", action="store_true", help="executa de verdade")
    p_ren.set_defaults(func=_cmd_renomear)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, OSError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
