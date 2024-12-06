import sys
import typer
from typing import Annotated, List, IO


class LineFormatter:
    def __init__(self, add_line_number: bool = False):
        self.add_line_number = add_line_number
        self.counter = 1

    def format(self, line: str):
        if self.add_line_number:
            formatted_line = f"\t{self.counter} {line}"
            self.counter += 1
            return formatted_line
        else:
            return line


def read_from_file(file: IO):
    for line in file:
        yield line


def read_from_stdin():
    for line in sys.stdin.readlines():
        yield line


def read_from_stdin_interactive():
    while True:
        try:
            line = input()
            yield line + "\n"
        except EOFError:
            break


def process_lines(lines: List[str], formatter: LineFormatter):
    for line in lines:
        print(formatter.format(line), end="")


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
    formatter = LineFormatter(add_line_number)

    if args:
        for filename in args:
            if filename == "-":
                # read from standard input
                lines = read_from_stdin_interactive()
                process_lines(lines, formatter)
            else:
                try:
                    with open(filename, "r") as file:
                        lines = read_from_file(file)
                        process_lines(lines, formatter)
                except FileNotFoundError:
                    print(f"\nhcat: File {filename} doesn't exist", end="\n\n")
                except PermissionError:
                    print(f"\nhcat: File {filename} cannot be accessed", end="\n\n")

    elif not sys.stdin.isatty():
        # Data is being piped to standard input
        lines = read_from_stdin()
        process_lines(lines, formatter)
    else:
        # Receiving input from stdin and printing it immediately
        lines = read_from_stdin_interactive()
        process_lines(lines, formatter)


def entry_point() -> None:
    typer.run(main)


if __name__ == "__main__":
    typer.run(main)
