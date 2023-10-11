"""Arquivo que estudantes não devem editar"""

import os
from fnmatch import fnmatch

import typer
from rich import print
from rich.panel import Panel
from typing_extensions import Annotated

from pro_filer import actions


typer_app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)


def scrape_paths(path, patterns_to_ignore):
    all_files = []
    all_dirs = []
    for root, dirs, files in os.walk(path):
        clear_ignored_dirs(patterns_to_ignore, dirs)
        all_dirs.extend([os.path.join(root, dir) for dir in dirs])
        all_files.extend(get_file_paths(patterns_to_ignore, root, files))

    return all_files, all_dirs


def get_patterns_to_ignore(patterns_file=".gitignore"):
    try:
        with open(patterns_file, "r") as f:
            file_lines = f.readlines()
    except FileNotFoundError:
        return set()

    return {
        line.strip()
        for line in file_lines
        if not line.startswith("#") and line.strip() != ""
    }


def clear_ignored_dirs(patterns_to_ignore, dirs):
    for dir in dirs[:]:
        if dir == ".git" or is_ignored_path(patterns_to_ignore, dir):
            dirs.remove(dir)


def get_file_paths(patterns_to_ignore, root, files):
    sub_all_files = []
    for file in files:
        if not is_ignored_path(patterns_to_ignore, file):
            sub_all_files.append(os.path.join(root, file))
    return sub_all_files


def is_ignored_path(patterns_to_ignore, file):
    return any(
        fnmatch(file, pattern.rstrip("/")) for pattern in patterns_to_ignore
    )


@typer_app.command("classify-by", help="Classify files by criteria")
def classify_files(
    ctx: typer.Context,
    criteria: Annotated[
        str,
        typer.Argument(
            ...,
            help="Criteria to classify files",
            autocompletion=lambda: ["name", "extension", "size"],
        ),
    ],
):
    print(actions.classify_files(ctx.obj, by=criteria))


@typer_app.command("search-file", help="Search files by name")
def search_files_by_name(
    ctx: typer.Context,
    search_term: Annotated[
        str, typer.Argument(..., help="Search term to match file names")
    ],
    case_sensitive: Annotated[
        bool, typer.Option(help="Choose if search is case sensitive or not")
    ] = True,
):
    print(actions.find_file_by_name(ctx.obj, search_term, case_sensitive))


@typer_app.command("find-duplicate", help="Show duplicate files")
def show_duplicate_files(ctx: typer.Context):
    print(actions.find_duplicate_files(ctx.obj))


@typer_app.command("tree", help="Show tree of files and directories")
def show_tree(ctx: typer.Context):
    actions.show_tree(ctx.obj)


@typer_app.command("disk-usage", help="Show disk usage")
def show_disk_usage(ctx: typer.Context):
    actions.show_disk_usage(ctx.obj)


@typer_app.command("file-details", help="Show file details")
def show_file_details(ctx: typer.Context):
    actions.show_details(ctx.obj)


@typer_app.command("deepest-file", help="Find the deepest file")
def deepest_file(ctx: typer.Context):
    actions.show_deepest_file(ctx.obj)


@typer_app.command(help="Shows a preview of the path")
def preview(ctx: typer.Context):
    actions.show_preview(ctx.obj)


@typer_app.callback()
def main(
    path: Annotated[str, typer.Argument(..., help="Path to be processed")],
    ctx: typer.Context,
):
    print(
        Panel(
            f"Processing path: '{path}'",
            title="ProFiler",
            title_align="left",
            border_style="green",
            highlight=True,
            expand=False,
        )
    )

    patterns_to_ignore = get_patterns_to_ignore()

    file_paths, dir_paths = scrape_paths(path, patterns_to_ignore)

    ctx.obj = {
        "base_path": path,
        "all_files": file_paths,
        "all_dirs": dir_paths,
    }
