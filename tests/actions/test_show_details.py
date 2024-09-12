import os
from unittest.mock import Mock, patch
from pro_filer.actions.main_actions import show_details  # NOQA


def test_show_details_non_existent_file(capsys):
    context = {"base_path": "any", "all_dirs": [], "all_files": []}

    show_details(context)

    assert capsys.readouterr().out == "File 'any' does not exist\n"


def test_show_details_directory(capsys, tmp_path):
    base_path = tmp_path / "src/utils"
    base_path.mkdir(parents=True)

    (tmp_path / "src" / "__init__.py").touch()
    (tmp_path / "src" / "app.py").touch()
    (tmp_path / "src" / "utils" / "__init__.py").touch()

    context = {
        "base_path": str(base_path),
        "all_files": [
            "src/__init__.py",
            "src/app.py",
            "src/utils/__init__.py",
        ],
        "all_dirs": ["src", "src/utils"],
    }

    mock_date = Mock(return_value=1726178432.7637057)

    with patch("os.path.getmtime", mock_date):
        show_details(context)

    assert (
        capsys.readouterr().out
        == f"File name: utils\nFile size in bytes: {os.path.getsize(str(base_path))}\nFile type: directory\nFile extension: [no extension]\nLast modified date: 2024-09-12\n"
    )


def test_show_details_file(capsys, tmp_path):
    base_path = tmp_path / "src/app.py"
    base_path.parent.mkdir(parents=True)

    (tmp_path / "src" / "__init__.py").touch()
    base_path.touch()

    context = {
        "base_path": str(base_path),
        "all_files": [
            "src/__init__.py",
            "src/app.py",
        ],
        "all_dirs": ["src"],
    }

    mock_date = Mock(return_value=1726178432.7637057)

    with patch("os.path.getmtime", mock_date):
        show_details(context)

    assert (
        capsys.readouterr().out
        == f"File name: app.py\nFile size in bytes: {os.path.getsize(str(base_path))}\nFile type: file\nFile extension: .py\nLast modified date: 2024-09-12\n"
    )
