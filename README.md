# KHOADE Toolkit

Pequena caixa de ferramentas de linha de comando para o dia a dia. Feita só com a biblioteca padrão do Python, sem dependências externas.

## Ferramentas

| Comando | O que faz |
| --- | --- |
| `khoade hash` | Calcula o hash (MD5, SHA-1, SHA-256, SHA-512) de um ou mais arquivos |
| `khoade senha` | Gera senhas aleatórias seguras (módulo `secrets`) |
| `khoade organizar` | Separa os arquivos de uma pasta em subpastas por tipo |
| `khoade renomear` | Renomeia arquivos em lote com prefixo e numeração |

`organizar` e `renomear` rodam em **modo simulação** por padrão: só mostram o que seria feito. Use `--aplicar` para executar de verdade.

## Instalação

Requer Python 3.8 ou superior.

```bash
git clone https://github.com/KHOADE-V/KHOADE-TOOLKIT.git
cd KHOADE-TOOLKIT
pip install -e .
```

Sem instalar, também funciona com `python -m khoade_toolkit <comando>`.

## Exemplos

```bash
# hash de um arquivo
khoade hash arquivo.iso -a sha256

# 3 senhas de 20 caracteres
khoade senha -t 20 -n 3

# ver como a pasta Downloads seria organizada
khoade organizar ~/Downloads
# executar de verdade
khoade organizar ~/Downloads --aplicar

# renomear fotos para ferias_001.jpg, ferias_002.jpg...
khoade renomear ./fotos -p ferias_ --aplicar
```

## Testes

```bash
python -m unittest discover -s tests -v
```

## Licença

MIT. Veja o arquivo `LICENSE`.
