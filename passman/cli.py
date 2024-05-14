import os
import typer
import string
import secrets
import tempfile
import subprocess
from . import errors
from rich import print
from typing import List
from rich.prompt import Prompt
from typing_extensions import Annotated
from .passman import PASSMAN_DIR, PassMan

app = typer.Typer()

@app.command()
def init(gpg_id: List[str]):
    """Initializes PassMan vault"""

    if not os.path.exists(PASSMAN_DIR):
        os.makedirs(PASSMAN_DIR)

    with open(os.path.join(PASSMAN_DIR, ".gpg_id"), "w") as f:
        for id in gpg_id:
            f.write(id + "\n")

    print(f"Vault [bold green]initialized[/] for [bold italic]{' '.join(gpg_id)}[/], it can be found at '{PASSMAN_DIR}'")

@app.command()
def add(login: str):
    """Add existing passwords to vault"""

    if PassMan.entry_exists(login):
        errors.EntryAlreadyExists(login)

    entry = PassMan.get_entry_path(login)
    gpg_id = PassMan.get_gpg_id()

    password = Prompt.ask(f"Enter password for [bold]'{login}'[/]", password=True)
    confirm = Prompt.ask(f"Confirm password for [bold]'{login}'[/]", password=True)

    if not password == confirm:
        raise errors.PasswordsDontMatch()
    
    PassMan.create_entry(login, password, gpg_id)

    print(f"[bold green]Added[/] existing password at '{entry}'")

@app.command()
def generate(
    login: str,
    length: Annotated[int, typer.Argument()] = 16):
    """Generate new login to vault"""

    if PassMan.entry_exists(login): 
        errors.EntryAlreadyExists(login)
    
    gpg_id = PassMan.get_gpg_id()
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))

    PassMan.create_entry(login, password, gpg_id)
    print(f"[bold green]Generated[/] password for '{login}' is [bold]{password}[/]")

@app.command()
def view(login: str):
    """View specific login from vault"""

    if not PassMan.is_initialized(): 
        raise errors.NotInitialized()
    if not PassMan.entry_exists(login): 
        raise errors.EntryNotFound(login)

    password = PassMan.get_entry(login)
    
    print(f"[bold]Login:[/] {login}\n[bold]Password:[/] {password.data.decode()}")

@app.command()
def rm(login: str):
    """Remove existing passwords from vault"""

    if not PassMan.is_initialized(): 
        raise errors.NotInitialized()
    if not PassMan.entry_exists(login): 
        raise errors.EntryNotFound(login)

    os.remove(PassMan.get_entry_path(login))
    print(f"[bold red]Removed[/] '{login}' entry")

@app.command()
def edit(login: str):
    """Edit specific entry content"""

    if not PassMan.is_initialized(): 
        raise errors.NotInitialized()
    if not PassMan.entry_exists(login): 
        raise errors.EntryNotFound(login)
    
    password = PassMan.get_entry(login)
    gpg_id = PassMan.get_gpg_id()
    
    with tempfile.NamedTemporaryFile(mode="w", delete = False) as changes_file:
        changes_file.write(password.data.decode())

    try:
        process = subprocess.Popen(["notepad.exe", changes_file.name])
        process.wait()

        changes = PassMan.get_file_content(changes_file.name)
        PassMan.create_entry(login, changes, gpg_id)

        print(f"[bold green]Edited[/] '{login}' entry")
    finally:
        os.remove(changes_file.name)

@app.command()
def ls():
    """List all passwords from vault"""

    if not PassMan.is_initialized(): 
        raise errors.NotInitialized()

    for root, dirs, files in os.walk(PASSMAN_DIR):
        indent_level = root.replace(PASSMAN_DIR, "").count(os.sep)
        indentation = " " * 2 * indent_level
        base_root_name = os.path.basename(root)

        if indent_level < 2:
            if not base_root_name == ".passman":
                print(f'[bold]\[{base_root_name}][/]')
        else:
            print(f'[bold]{indentation}\[{base_root_name}][/]')

        for file in files:
            if not file == ".gpg_id" and file.endswith(".gpg"): 
                print(f'{indentation} => {os.path.basename(file).split(".gpg")[0]}')

if __name__ == "__main__":
    app()