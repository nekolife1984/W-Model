#!/usr/bin/env python3
"""Safely install the W-Model guidance listed in the distribution manifest."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import stat
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "scripts" / "w_model_install_manifest.json"
PROTECTED = {"AGENTS.md", ".agents/project.json"}


class InstallError(Exception):
    """Installation cannot safely continue."""


def ordinary(path: Path, *, directory: bool = False, optional: bool = False) -> bool:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        if optional:
            return False
        raise InstallError(f"必要なパスがありません: {path}")
    if stat.S_ISLNK(mode):
        raise InstallError(f"symlinkは使用できません: {path}")
    if not (stat.S_ISDIR(mode) if directory else stat.S_ISREG(mode)):
        raise InstallError(f"通常の{'ディレクトリ' if directory else 'ファイル'}ではありません: {path}")
    return True


def relative_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not value or any(part in ("", ".", "..") for part in value.split("/")):
        raise InstallError(f"安全でない導入先パスです: {value}")
    if value in PROTECTED:
        raise InstallError(f"保護対象は導入できません: {value}")
    return path


def check_parents(root: Path, relative: Path) -> Path:
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        if ordinary(current, directory=True, optional=True):
            continue
        if current.exists():
            raise InstallError(f"親パスがディレクトリではありません: {current}")
    return root / relative


def load_manifest() -> list[str]:
    try:
        value = json.loads(MANIFEST.read_text(encoding="utf-8"))
        files = value["files"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise InstallError(f"マニフェストを読み込めません: {exc}") from exc
    if not isinstance(files, list) or not all(isinstance(item, str) for item in files):
        raise InstallError("マニフェストのfilesは文字列配列である必要があります")
    if len(files) != len(set(files)):
        raise InstallError("マニフェストに重複したパスがあります")
    for item in files:
        relative_path(item)
        source = check_parents(REPO_ROOT, Path(item))
        ordinary(source)
    return files


def classify(root: Path, files: list[str]) -> tuple[dict[str, str], list[str]]:
    statuses: dict[str, str] = {}
    conflicts: list[str] = []
    for item in files:
        destination = check_parents(root, relative_path(item))
        if not ordinary(destination, optional=True):
            statuses[item] = "追加"
            continue
        source = REPO_ROOT / item
        if source.read_bytes() == destination.read_bytes():
            statuses[item] = "同一"
        else:
            statuses[item] = "競合"
            conflicts.append(item)
    return statuses, conflicts


def apply(root: Path, additions: list[str]) -> None:
    created: list[Path] = []
    created_dirs: list[Path] = []
    try:
        for item in additions:
            destination = root / relative_path(item)
            missing: list[Path] = []
            parent = destination.parent
            while parent != root and not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for directory in reversed(missing):
                directory.mkdir()
                created_dirs.append(directory)
            content = (REPO_ROOT / item).read_bytes()
            fd, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(content)
                    stream.flush()
                    os.fsync(stream.fileno())
                if destination.exists() or destination.is_symlink():
                    raise InstallError(f"書き込み直前に競合が発生しました: {item}")
                os.replace(temporary, destination)
                created.append(destination)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
    except (OSError, InstallError) as exc:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        for path in reversed(created_dirs):
            try:
                path.rmdir()
            except OSError:
                pass
        raise InstallError(f"コピーに失敗しました。作成済みファイルをロールバックしました: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="導入先Repositoryのルート")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="計画だけを表示（デフォルト）")
    mode.add_argument("--apply", action="store_true", help="確認したファイルをコピー")
    args = parser.parse_args(argv)
    try:
        target = args.target.expanduser().resolve(strict=True)
        ordinary(target, directory=True)
        files = load_manifest()
        statuses, conflicts = classify(target, files)
    except (OSError, InstallError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 2

    print(f"対象: {target}")
    print("モード: 適用" if args.apply else "モード: dry-run（ファイル変更なし）")
    for item, status in statuses.items():
        print(f"[{status}] {item}")
        if status == "競合":
            diff = difflib.unified_diff(
                (target / item).read_text(encoding="utf-8", errors="replace").splitlines(keepends=True),
                (REPO_ROOT / item).read_text(encoding="utf-8", errors="replace").splitlines(keepends=True),
                fromfile="既存", tofile="W-Model提案",
            )
            print("".join(diff))
    if conflicts:
        print("競合があるため、全ての書き込みを停止しました:")
        for item in conflicts:
            print(f"  - {item}")
        return 1
    if not args.apply:
        print("適用するには同じコマンドに --apply を指定してください。")
        return 0
    additions = [item for item, status in statuses.items() if status == "追加"]
    try:
        apply(target, additions)
    except InstallError as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 2
    print(f"導入完了: {len(additions)}ファイルを追加しました。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
