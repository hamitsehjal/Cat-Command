import sys
import typer
from typing_extensions import Annotated, List


def main(
    args: Annotated[
        List[str], typer.Argument(help="List of filenames to concatenate")
    ] = None
):
    if args is not None:
        for filename in args:
            try:
                if filename == "-":
                    # read from standard input
                    continue
                with open(file=filename, mode="r") as file:
                    content = file.read()
                    print(content, end="")
            except FileNotFoundError:
                print(f"\nhcat: File {filename} doesn't exist", end="\n\n")
            except PermissionError:
                print(f"\nhcat: File {filename} cannot be accessed", end="\n\n")

    if not sys.stdin.isatty():
        # Data is being piped to standard input
        for line in sys.stdin:
            print(line, end="")


def entry_point() -> None:
    typer.run(main)


if __name__ == "__main__":
    typer.run(main)
