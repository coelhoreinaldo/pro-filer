from pathlib import Path
import pytest
from pro_filer.actions.main_actions import find_duplicate_files  # NOQA


def test_find_no_files():
    context = {
        "all_files": [
            ".gitignore",
            "src/app.py",
            "src/utils/__init__.py",
        ]
    }
    with pytest.raises(ValueError, match="All files must exist"):
        find_duplicate_files(context)


def test_find_no_duplicate_files(tmp_path):
    context = {
        "all_files": [
            str(tmp_path / "src/utils/.gitignore"),
            str(tmp_path / "src/utils/__init__.py"),
            str(tmp_path / "src/app.py"),
        ]
    }

    for i, file in enumerate(context["all_files"]):
        file_path = Path(file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
        file_path.write_text(f"hello = world {i}")

    assert find_duplicate_files(context) == []


def test_find_duplicate_files(tmp_path):
    utils_app = tmp_path / "src/utils/app.py"
    src_app = tmp_path / "src/app.py"

    context = {
        "all_files": [
            str(utils_app),
            str(tmp_path / "src/utils/__init__.py"),
            str(src_app),
        ],
    }

    for file in context["all_files"]:
        file_path = Path(file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()

    utils_app.write_text("hello = world")
    src_app.write_text("hello = world")

    assert find_duplicate_files(context) == [(str(utils_app), str(src_app))]
