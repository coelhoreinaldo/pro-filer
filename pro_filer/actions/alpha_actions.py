"""Arquivo que estudantes não devem editar"""

import os


def _classify_files_by_name(context):
    classified_files = {}

    for path in context["all_files"]:
        extension = path.split(".")[-1]
        extension_length = len(extension)
        file_name = path.split("/")[-1][: -extension_length - 1]

        if file_name not in classified_files:
            classified_files[file_name] = []

        classified_files[file_name].append(path)

    return classified_files


def _classify_files_by_size(context):
    classified_files = {}
    for path in context["all_files"]:
        file_size = str(os.path.getsize(path))

        if file_size not in classified_files:
            classified_files[file_size] = []

        classified_files[file_size].append(path)

    return classified_files


def _classify_files_by_extension(context):
    classified_files = {}

    for path in context["all_files"]:
        file_extension = path.split(".")[-1].lower()

        if file_extension not in classified_files:
            classified_files[file_extension] = []

        classified_files[file_extension].append(path)

    return classified_files


def classify_files(context, by):
    if by == "name":
        return _classify_files_by_name(context)
    if by == "size":
        return _classify_files_by_size(context)
    if by == "extension":
        return _classify_files_by_extension(context)

    raise ValueError("Invalid criteria to classify files")


def _print_curr_dir(start_path, root, level):
    indent = ("│   " * (level)) + "└──"
    if not start_path == root:
        print(f"{indent}{os.path.basename(root)}/")


def _print_inner_files(context, files, level):
    subindent = ("│   " * (level + 1)) + "└──"
    for f in files:
        if not any(
            f in included_file for included_file in context["all_files"]
        ):
            continue
        print(f"{subindent}{f}")


def show_tree(context):
    start_path = context["base_path"]
    print(start_path)
    for root, dirs, files in os.walk(start_path):
        if not any(
            root in included_dirs for included_dirs in context["all_dirs"]
        ):
            continue
        level = root.replace(start_path, "").count(os.sep)
        _print_curr_dir(start_path, root, level)
        _print_inner_files(context, files, level)
