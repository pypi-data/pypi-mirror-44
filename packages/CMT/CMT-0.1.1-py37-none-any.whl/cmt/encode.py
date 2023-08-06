from pathlib import Path


def encode(file: Path, cmap):
    with file.open("wb") as writer:
        writer.write(cmap.encode())
