import typer

app = typer.Typer()


@app.command()
def run_twitter(use_dot_env: bool):
    typer.echo(f"Use dot env {use_dot_env}")


if __name__ == "__main__":
    app()
