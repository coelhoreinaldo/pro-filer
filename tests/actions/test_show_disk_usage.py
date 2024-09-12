from unittest.mock import Mock, patch
from pro_filer.actions.main_actions import show_disk_usage  # NOQA


def test_show_disk_usage(capsys, tmp_path):
    base_path = tmp_path / "src/utils"
    base_path.mkdir(parents=True)

    (tmp_path / "src" / "__init__.py").touch()
    app_py = tmp_path / "src" / "app.py"
    app_py.write_text("hello = world")

    context = {
        "base_path": str(base_path),
        "all_files": [
            str(tmp_path / "src" / "__init__.py"),
            str(tmp_path / "src" / "app.py"),
        ],
        "all_dirs": [str(tmp_path / "src"), str(tmp_path / "src" / "utils")],
    }

    with patch(
        "pro_filer.actions.main_actions._get_printable_file_path",
        Mock(side_effect=lambda x: x.split("test_show_disk_usage0/")[1]),
    ):
        show_disk_usage(context)
        captured = capsys.readouterr()

        assert captured.out == (
            "'src/app.py':                                                          13 (100%)\n"
            "'src/__init__.py':                                                     0 (0%)\n"
            "Total size: 13\n"
        )
