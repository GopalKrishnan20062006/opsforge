import typer
from opsforge.doctor import check_tool, check_docker_running

app = typer.Typer()


@app.command()
def doctor():
    tools = [
        ("python3", "Python"),
        ("git", "Git"),
        ("docker", "Docker"),
        ("make", "Make"),
    ]

    for cmd, name in tools:
        if check_tool(cmd):
            print(f"✓ {name}")
        else:
            print(f"✗ {name}")

    if check_docker_running():
        print("✓ Docker daemon running")
    else:
        print("✗ Docker daemon not running")
@app.command()
def hello():
	print("Hello")

if __name__ == "__main__":
    app()
