"""Arquivo que estudantes não devem editar"""

from typing import List, TypedDict


class Context(TypedDict):
    base_path: str
    all_files: List[str]
    all_dirs: List[str]
