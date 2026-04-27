from pathlib import Path

def list_directory_files(path):
    # dabūjam direktoriju, no kuras tiek palaists aģents
    workplace_root = Path.cwd().resolve()
    # mēginam dabūt īstās direktorijas ceļu
    candidate = (workplace_root / path).resolve()

    # aģents spēs nolasīt tikai to direktoriju, kas ir iekšā aģenta direktorijā
    if workplace_root not in [candidate, *candidate.parents]:
        return f"Path escapes the worplace root: {path}"

    if not candidate.exists():
        return f"Path does not exist: {path}"

    if not candidate.is_dir():
        return f"Not a directory: {path}"

    entries = []
    for item in candidate.iterdir():
        kind = "dir" if item.is_dir() else "file"
        relative = item.relative_to(workplace_root)
        entries.append(f"{kind}: {relative}")

    return "\n".join(entries) if entries else "empty directory."
