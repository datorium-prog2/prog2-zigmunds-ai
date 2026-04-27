from pathlib import Path

WORKPLACE_ROOT = Path.cwd().resolve()


# funkcija, kas atrod direktoriju / failu pēc ceļā (path)
def _resolve_path(path):
    # mēginam dabūt īstās direktorijas ceļu
    file = (WORKPLACE_ROOT / path).resolve()

    # aģents spēs nolasīt tikai to direktoriju, kas ir iekšā aģenta direktorijā
    if WORKPLACE_ROOT not in [file, *file.parents]:
        raise ValueError(f"Path escapes the worplace root: {path}")

    return file


# parāda atrastās direktorijas failus
def list_directory_files(path="."):
    try:
        directory = _resolve_path(path)
    except ValueError as err:
        return str(err)

    if not directory.exists():
        return f"Path does not exist: {path}"
    if not directory.is_dir():
        return f"Not a directory: {path}"

    entries = []
    for item in directory.iterdir():
        kind = "dir" if item.is_dir() else "file"
        relative = item.relative_to(WORKPLACE_ROOT)
        entries.append(f"{kind}: {relative}")

    return "\n".join(entries) if entries else "empty directory."


def read_file(path):
    target = _resolve_path(path)

    if not target.exists():
        return f"Path does not exist: {path}"
    if not target.is_file():
        return f"Not a file: {path}"

    return target.read_text(encoding="utf-8")


def write_file(path, content):
    target = _resolve_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} characters to {target.relative_to(WORKPLACE_ROOT)}"
