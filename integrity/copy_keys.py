import shutil
from pathlib import Path


def main():
    source = Path.cwd()
    destination = Path("../../projects/178.154.210.253_gtcl")
    shutil.copy(source / "private.key", destination / "private.key")
    shutil.copy(source / "public.key", destination / "public.key")


if __name__ == "__main__":
    main()
