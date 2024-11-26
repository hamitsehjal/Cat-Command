import sys
import typer
from typing_extensions import Annotated, List


def print_loop() -> None:
    try:
        while True:
            text = input()
            print(text)
    except EOFError:
        sys.stdout.flush()


def print_file(file, add_line_number: bool = False) -> None:
    if add_line_number:
        counter = 1
        for line in file:
            print(f"{counter}: {line}", end="")
            counter += 1
    else:
        for line in file:
            print(line, end="")


def print_text(add_line_number=False) -> None:
    if add_line_number:
        counter = 1
        for line in sys.stdin:
            print(f"{counter}: {line}", end="")
            counter += 1
    else:
        for line in sys.stdin:
            print(line, end="")


def main(
    args: Annotated[
        List[str], typer.Argument(help="List of filenames to concatenate")
    ] = None,
    add_line_number: Annotated[
        bool,
        typer.Option(
            "-n",
            "--number",
            help="Add Line Numbers",
            rich_help_panel="Customization and Utils",
        ),
    ] = False,
) -> None:
    if args is not None:
        for filename in args:
            try:
                if filename == "-":
                    # read from standard input
                    print_loop()
                else:
                    with open(filename, "r") as file:
                        print_file(file, add_line_number)

            except FileNotFoundError:
                print(f"\nhcat: File {filename} doesn't exist", end="\n\n")
            except PermissionError:
                print(f"\nhcat: File {filename} cannot be accessed", end="\n\n")

    elif not sys.stdin.isatty():
        # Data is being piped to standard input
        print_text(add_line_number)
    else:
        # Receiving input from stdin and printing it immediately
        print_loop()


def entry_point() -> None:
    typer.run(main)


if __name__ == "__main__":
    typer.run(main)
