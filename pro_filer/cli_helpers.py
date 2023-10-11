"""Arquivo que estudantes não devem editar"""


def _get_printable_file_path(file_path):
    if len(file_path) > 60:
        return file_path[:27] + "..." + file_path[-30:]
    else:
        return file_path
