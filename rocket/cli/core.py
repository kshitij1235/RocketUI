import os
import platform
import shutil
import subprocess
import sys
import time
from enum import Enum
from pathlib import Path
from typing import Iterable, Optional

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

# ============================================================
# Target OS detection
# ============================================================


class TargetOS(Enum):
    LINUX = "linux"
    WINDOWS = "windows"
    MAC = "mac"


def detect_os() -> TargetOS:
    system = platform.system().lower()

    if system == "linux":
        return TargetOS.LINUX
    if system == "windows":
        return TargetOS.WINDOWS
    if system == "darwin":
        return TargetOS.MAC

    raise RuntimeError(f"Unsupported operating system: {system}")


# ============================================================
# Hot reload
# ============================================================


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, process: subprocess.Popen[str]) -> None:
        self._process = process

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory or not event.src_path.endswith(".py"):
            return

        if self._process.poll() is None:
            self._process.terminate()

        self._process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )


def hot_reload_app(path: str = ".") -> None:
    process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    observer = Observer()
    observer.schedule(ReloadHandler(process), path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if process.poll() is None:
            process.terminate()

    observer.join()


def run_app() -> subprocess.Popen[bytes]:
    """
    Launch the application normally (no hot reload).
    """
    return subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )


# ============================================================
# Cleanup
# ============================================================


def cleanup(
    *,
    files_to_remove: Iterable[str] = (),
    dirs_to_remove: Iterable[str] = (),
    file_extensions: Iterable[str] = (),
    root: Optional[Path] = None,
) -> None:
    base = root or Path.cwd()

    for path in base.rglob("*"):
        try:
            if path.is_file():
                if path.name in files_to_remove or any(
                    path.name.endswith(ext) for ext in file_extensions
                ):
                    path.unlink()

            elif path.is_dir() and path.name in dirs_to_remove:
                shutil.rmtree(path)

        except OSError as exc:
            print(f"Cleanup error: {path} ({exc})", file=sys.stderr)


# ============================================================
# PyInstaller build (auto OS)
# ============================================================


def create_executable(
    *,
    script_path: Path,
    resource_dir: Path,
    output_root: Path,
    onefile: bool = True,
    windowed: bool = True,
) -> None:
    if not script_path.is_file():
        raise FileNotFoundError(script_path)
    if not resource_dir.is_dir():
        raise FileNotFoundError(resource_dir)

    target = detect_os()

    output_dir = output_root / target.value
    dist_dir = output_dir / "dist"
    work_dir = output_dir / "work"

    dist_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    command: list[str] = ["pyinstaller"]

    if onefile:
        command.append("--onefile")

    if windowed:
        command.append("--noconsole")

    command.extend(
        [
            str(script_path),
            f"--add-data={resource_dir}{os.pathsep}resources/images",
            f"--distpath={dist_dir}",
            f"--workpath={work_dir}",
            "--clean",
        ]
    )

    subprocess.run(command, check=True)


# ============================================================
# Nuitka build (optional / future)
# ============================================================


def create_executable_nuitka(
    *,
    script_path: Path,
    resource_dir: Path,
    output_root: Path,
    onefile: bool = True,
) -> None:
    if not script_path.is_file():
        raise FileNotFoundError(script_path)
    if not resource_dir.is_dir():
        raise FileNotFoundError(resource_dir)

    target = detect_os()
    output_dir = output_root / target.value
    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        "nuitka",
        "--standalone",
        "--onefile" if onefile else "",
        "--output-dir",
        str(output_dir),
        str(script_path),
        "--include-data-dir",
        f"{resource_dir}=resources/images",
    ]

    command = [arg for arg in command if arg]

    subprocess.run(command, check=True)


# ============================================================
# Resource path (runtime-safe)
# ============================================================


def resource_path(relative_path: str | Path) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path.cwd()))
    return base / relative_path
