from pro_filer.actions.main_actions import show_preview


def test_show_preview_empty_context(capsys):
    empty_context = {"all_dirs": [], "all_files": []}
    show_preview(empty_context)
    captured = capsys.readouterr()

    assert captured.out == "Found 0 files and 0 directories\n"


def test_show_preview_without_dirs(capsys):
    context_without_dirs = {
        "all_files": [
            "__init__.py",
            "app.py",
            "__init__.py",
        ],
        "all_dirs": [],
    }

    show_preview(context_without_dirs)
    captured = capsys.readouterr()

    assert (
        captured.out
        == "Found 3 files and 0 directories\nFirst 5 files: ['__init__.py', 'app.py', '__init__.py']\nFirst 5 directories: []\n"
    )


def test_show_preview(capsys):
    context = {
        "all_files": [
            "src/__init__.py",
            "src/app.py",
            "src/utils/__init__.py",
        ],
        "all_dirs": ["src", "src/utils"],
    }

    show_preview(context)
    captured = capsys.readouterr()

    assert (
        captured.out
        == "Found 3 files and 2 directories\nFirst 5 files: ['src/__init__.py', 'src/app.py', 'src/utils/__init__.py']\nFirst 5 directories: ['src', 'src/utils']\n"
    )


def test_show_preview_more_than_five_files_or_directories(capsys):
    context = {
        "all_files": [
            "/path/to/file.sql",
            "/path/to/file.txt",
            "/path/to/file2.txt",
            "/path/to/FILE.txt",
            "/path/to/FILE2.TXT",
            "/path/to/something.txt",
            "/path-to/file.txt",
        ],
        "all_dirs": ["path", "to", "path-to"],
    }

    show_preview(context)
    message = capsys.readouterr().out

    assert "something" not in message
