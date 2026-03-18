"""Console script for instructor_examples."""

import typer
from rich.console import Console

from instructor_examples import utils

app = typer.Typer()
console = Console()


@app.command()
def main(
    remote_repo_folder: str = typer.Argument(..., help="Input remote_repo_folder path."),
    out_folder: str = typer.Option(None, help="Optional output folder."),
    repo: str = typer.Option(None, help="Optional repo path."),
) -> None:
    """Console script for instructor_examples."""
    console.print(f"Input remote_repo_folder: {remote_repo_folder}")

    if out_folder:
        console.print(f"Output folder: {out_folder}")
    else:
        console.print("No output folder specified. Using current folder.")

    utils.run(
        remote_repo_folder=remote_repo_folder,
        out_folder=out_folder,
        repo=repo,
        console=console,
    )


if __name__ == "__main__":
    app()
