"""Arquivo que estudantes não devem editar"""

from datetime import date
import filecmp
import itertools
from pro_filer.cli_helpers import _get_printable_file_path
import os


def find_duplicate_files(context):
    """
    Encontra arquivos duplicados, comparando todos os arquivos entre si.
    Retorna uma lista de tuplas com os pares de arquivos duplicados.
    """

    all_files = context["all_files"]
    duplicate_files = []

    for file1, file2 in itertools.combinations(all_files, 2):
        try:
            if filecmp.cmp(file1, file2, shallow=False):
                duplicate_files.append((file1, file2))
        except FileNotFoundError:
            raise ValueError("All files must exist")

    return duplicate_files


def show_details(context):
    """Mostra detalhes do arquivo ou diretório"""
    file_path = context["base_path"]
    file_name = file_path.split("/")[-1]

    if not os.path.exists(file_path):
        print(f"File '{file_name}' does not exist")
        return

    print(f"File name: {file_name}")
    print(f"File size in bytes: {os.path.getsize(file_path)}")
    print(f"File type: {'directory' if os.path.isdir(file_path) else 'file'}")

    _, file_extension = os.path.splitext(file_name)

    print(f"File extension: {file_extension or '[no extension]'}")

    py_mod_date = date.fromtimestamp(os.path.getmtime(file_path))

    print(f"Last modified date: {py_mod_date}")


def show_disk_usage(context):
    """Mostra o uso de disco"""
    total_size = sum(os.path.getsize(file) for file in context["all_files"])

    for file_path in sorted(
        context["all_files"], key=os.path.getsize, reverse=True
    ):
        file_size = os.path.getsize(file_path)
        print(
            f"'{_get_printable_file_path(file_path)}':".ljust(70),
            f"{file_size} ({int(file_size / total_size * 100)}%)",
        )

    print(f"Total size: {total_size}")


def show_preview(context):
    """Mostra uma prévia dos detalhes do arquivo ou diretório"""

    print(
        f'Found {len(context["all_files"])} files '
        f'and {len(context["all_dirs"])} directories'
    )
    if context["all_files"] or context["all_dirs"]:
        print(f'First 5 files: {context["all_files"][:5]}')
        print(f'First 5 directories: {context["all_dirs"][:5]}')
