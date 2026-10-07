#!/usr/bin/env python3
"""Safely append the W-Model guidance section to a repository AGENTS.md."""

from __future__ import annotations

import difflib
import os
import re
import secrets
import stat
import sys
from pathlib import Path


TEMPLATE = Path(".agents/templates/w-model/AGENTS.md.template")
IDENTIFIER = "W-Model 開発案内"
HEADING = re.compile(r"^( {0,3})(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", re.MULTILINE)
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


class SetupError(Exception):
    """An unsafe or conflicting input prevented setup."""


def _ordinary(path: Path, *, directory: bool = False, optional: bool = False) -> bool:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        if optional:
            return False
        raise SetupError(f"必要なパスがありません: {path}")
    if stat.S_ISLNK(mode):
        raise SetupError(f"symlinkは使用できません: {path}")
    expected = stat.S_ISDIR(mode) if directory else stat.S_ISREG(mode)
    if not expected:
        raise SetupError(f"通常の{'ディレクトリ' if directory else 'ファイル'}ではありません: {path}")
    return True


def _read_utf8(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeError) as exc:
        raise SetupError(f"UTF-8として安全に読み込めません: {path}: {exc}") from exc


def _validate_link(root: Path, target: str) -> None:
    if target.startswith(("https://", "http://", "mailto:")) or target.startswith("#"):
        return
    if any(char.isspace() for char in target) or any(char in target for char in "<>\\%()"):
        raise SetupError(f"曖昧または符号化されたリンク先は使用できません: {target}")
    path_text = target.split("#", 1)[0].split("?", 1)[0]
    if not path_text:
        return
    link = Path(path_text)
    if link.is_absolute():
        raise SetupError(f"絶対パスリンクは使用できません: {target}")
    current = root
    for part in (Path(".") / link).parts:
        if part in ("", "."):
            continue
        if part == "..":
            current = current.parent
        else:
            current = current / part
        try:
            mode = current.lstat().st_mode
        except OSError as exc:
            raise SetupError(f"リンク先が存在しません: {target}") from exc
        if stat.S_ISLNK(mode):
            raise SetupError(f"リンク先にsymlinkがあります: {target}")
    if not current.is_relative_to(root) or not stat.S_ISREG(current.lstat().st_mode):
        raise SetupError(f"リンク先がRepository内の通常ファイルではありません: {target}")


def _headings(text: str) -> list[re.Match[str]]:
    fenced: list[tuple[int, int]] = []
    offset = 0
    fence_char: str | None = None
    fence_size = 0
    fence_start = 0
    for line in text.splitlines(keepends=True):
        fence = FENCE.match(line.rstrip("\r\n"))
        if fence:
            marker = fence.group(1)
            if fence_char is None and not (marker[0] == "`" and "`" in fence.group(2)):
                fence_char, fence_size = marker[0], len(marker)
                fence_start = offset
            elif fence_char == marker[0] and len(marker) >= fence_size and not fence.group(2).strip():
                fenced.append((fence_start, offset + len(line)))
                fence_char, fence_size = None, 0
        offset += len(line)
    if fence_char is not None:
        fenced.append((fence_start, len(text)))
    return [
        match for match in HEADING.finditer(text)
        if not any(start <= match.start() < end for start, end in fenced)
    ]


def _section_bounds(text: str, match: re.Match[str], headings: list[re.Match[str]]) -> tuple[int, int]:
    level = len(match.group(2))
    end = len(text)
    for candidate in headings:
        if candidate.start() <= match.start():
            continue
        if len(candidate.group(2)) <= level:
            end = candidate.start()
            break
    return match.start(), end


def _render(template: str, target: str) -> str:
    matches = _headings(template)
    if not matches or matches[0].group(3).strip() != IDENTIFIER or len(matches[0].group(2)) != 2:
        raise SetupError(f"テンプレート先頭に ## {IDENTIFIER} が必要です")
    if len([m for m in matches if m.group(3).strip() == IDENTIFIER]) != 1:
        raise SetupError("テンプレートの識別見出しが一意ではありません")
    start, end = _section_bounds(template, matches[0], matches)
    if template[:start].strip() or template[end:].strip():
        raise SetupError("テンプレートは単一セクションである必要があります")
    raw = template[start:end].rstrip("\r\n")
    level = len(matches[0].group(2))
    delta = target - level
    for heading in reversed(matches):
        shifted = len(heading.group(2)) + delta
        if shifted < 1 or shifted > 6:
            raise SetupError("挿入先の見出し階層ではテンプレート見出しがMarkdown範囲を超えます")
        raw = (
            raw[:heading.start() - start]
            + heading.group(1)
            + "#" * shifted
            + " "
            + heading.group(3).strip()
            + raw[heading.end() - start:]
        )
    return raw


def _write_atomic(root: Path, content: bytes, original: bytes | None, mode: int | None = None) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    root_fd = os.open(root, flags)
    temporary = f".AGENTS.md.{secrets.token_hex(8)}.tmp"
    try:
        temp_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(temporary, temp_flags, 0o600, dir_fd=root_fd)
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
            os.fchmod(stream.fileno(), stat.S_IMODE(mode) if mode is not None else 0o644)
        try:
            current_fd = os.open(
                "AGENTS.md",
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0),
                dir_fd=root_fd,
            )
        except FileNotFoundError:
            current = None
        else:
            if not stat.S_ISREG(os.fstat(current_fd).st_mode):
                os.close(current_fd)
                raise SetupError("書き込み直前にAGENTS.mdが通常ファイルでなくなりました")
            with os.fdopen(current_fd, "rb") as stream:
                current = stream.read()
        if current != original:
            raise SetupError("読み込み後にAGENTS.mdが変更されました。競合を避けるため書き込みを中止しました")
        os.replace(temporary, "AGENTS.md", src_dir_fd=root_fd, dst_dir_fd=root_fd)
    finally:
        try:
            os.unlink(temporary, dir_fd=root_fd)
        except FileNotFoundError:
            pass
        os.close(root_fd)


def setup(root: Path) -> str:
    root = root.absolute()
    _ordinary(root, directory=True)
    for directory in (root / ".agents", root / ".agents/templates", root / ".agents/templates/w-model"):
        _ordinary(directory, directory=True)
    template_path = root / TEMPLATE
    _ordinary(template_path)
    template = _read_utf8(template_path)
    for link in LINK.findall(template):
        _validate_link(root, link.strip())

    destination = root / "AGENTS.md"
    exists = _ordinary(destination, optional=True)
    original_mode = destination.lstat().st_mode if exists else None
    existing = _read_utf8(destination) if exists else ""
    headings = _headings(existing)
    matches = [m for m in headings if m.group(3).strip() == IDENTIFIER]
    if len(matches) > 1:
        rendered = _render(template, len(matches[0].group(2)))
        raise SetupError(_conflict(existing, rendered, "識別見出しが複数あります"))

    if matches:
        current_match = matches[0]
        begin, finish = _section_bounds(existing, current_match, headings)
        current = existing[begin:finish].strip("\r\n")
        expected = _render(template, len(current_match.group(2)))
        if current == expected:
            return "既に最新です (変更なし)"
        raise SetupError(_conflict(current, expected, "既存のW-Model案内がテンプレートと異なります"))

    top_level = min((len(m.group(2)) for m in headings), default=0)
    target_level = 1 if top_level == 0 else 2 if top_level == 1 else top_level
    rendered = _render(template, target_level)
    separator = "\n" if existing.endswith("\n") and not existing.endswith("\n\n") else "\n\n" if existing and not existing.endswith("\n\n") else ""
    updated = existing + separator + rendered + "\n"
    old_lines = existing.splitlines(keepends=True)
    new_lines = updated.splitlines(keepends=True)
    print("".join(difflib.unified_diff(old_lines, new_lines, fromfile="AGENTS.md", tofile="AGENTS.md (案)")))
    _write_atomic(root, updated.encode("utf-8"), existing.encode("utf-8") if exists else None, original_mode)
    verified = _read_utf8(destination)
    if verified != updated:
        raise SetupError("書き込み後の読み戻し内容が一致しません")
    return "AGENTS.mdを作成しました" if not exists else "AGENTS.mdに案内を追記しました"


def _conflict(current: str, expected: str, reason: str) -> str:
    diff = "".join(difflib.unified_diff(current.splitlines(True), expected.splitlines(True), fromfile="既存", tofile="テンプレート案"))
    return f"{reason}。書き込みを中止しました。\n{diff}"


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    try:
        print(setup(root))
    except (SetupError, OSError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
