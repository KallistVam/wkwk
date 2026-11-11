from pathlib import Path
import shutil


class FileManager:
    """Manages text files inside the simulator's virtual_files directory."""

    def __init__(self, directory=None):
        project_root = Path(__file__).resolve().parent.parent
        self.directory = Path(directory) if directory else project_root / "data" / "virtual_files"
        self.directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _safe_name(filename):
        if not isinstance(filename, str) or not filename.strip():
            return False
        name = filename.strip()
        return name not in {".", ".."} and Path(name).name == name and "/" not in name and "\\" not in name

    def _path(self, filename):
        if not self._safe_name(filename):
            return None
        return self.directory / filename.strip()

    def create_file(self, filename, content=""):
        path = self._path(filename)
        if path is None or path.exists():
            return False
        try:
            path.write_text(str(content), encoding="utf-8")
            return True
        except OSError:
            return False

    def read_file(self, filename):
        path = self._path(filename)
        if path is None or not path.is_file():
            return None
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return None

    def delete_file(self, filename):
        path = self._path(filename)
        if path is None or not path.is_file():
            return False
        try:
            path.unlink()
            return True
        except OSError:
            return False

    def rename_file(self, old_name, new_name):
        source, destination = self._path(old_name), self._path(new_name)
        if source is None or destination is None or not source.is_file() or destination.exists():
            return False
        try:
            source.rename(destination)
            return True
        except OSError:
            return False

    def copy_file(self, filename, new_name):
        source, destination = self._path(filename), self._path(new_name)
        if source is None or destination is None or not source.is_file() or destination.exists():
            return False
        try:
            shutil.copy2(source, destination)
            return True
        except OSError:
            return False

    def list_files(self):
        return sorted(
            item.name for item in self.directory.iterdir()
            if item.is_file()
        )
