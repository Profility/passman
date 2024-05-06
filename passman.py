import os
import sys
import gnupg
import typer
from typing_extensions import Annotated

HOME_DIR = os.path.expanduser("~")
PASSMAN_DIR = os.path.join(HOME_DIR, ".passman")
GPG_ID = os.path.join(PASSMAN_DIR, ".gpg_id")

gpg = gnupg.GPG()
app = typer.Typer()

def get_entry_path(entry):
    return os.path.join(PASSMAN_DIR, entry+".gpg")

def entry_exists(entry):
    return os.path.exists(get_entry_path(entry))

def get_gpg_id():
    with open(GPG_ID, "r") as f:
        return f.read()

@app.command()
def init(gpg_id: str):
    """
    Initializes PassMan vault
    """
    if os.path.exists(PASSMAN_DIR): 
        print("Vault already initialized, exiting...")
        sys.exit(1)
    else:
        os.makedirs(PASSMAN_DIR)
        with open(os.path.join(PASSMAN_DIR, ".gpg_id"), "w") as f:
            f.write(gpg_id)

    print(f"Vault initialized for {gpg_id}, it can be found at {PASSMAN_DIR}")

@app.command()
def insert(
    login: str,
    password: Annotated[str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)]):
    """
    Add existing passwords to vault
    """

    gpg_id = get_gpg_id()
    entry = get_entry_path(login)

    if entry_exists(login):
        overwrite_entry = input(f"An entry already exists for {login}. Overwrite it? [y/N]: ")
        if overwrite_entry.lower() == "n":
            sys.exit(0)

    gpg.encrypt(password, gpg_id, output=entry)
    gpg.encrypt(
        data=password,
        recipients=gpg_id,
        output=entry,
        armor=True
    )

    print("Password generated at %s", entry)
    ...

@app.command()
def view(
    login: str,
    passphrase: Annotated[str, typer.Option(prompt=True, hide_input=True)]):
    """
    View specific login from vault
    """
    if not entry_exists(login): print(f"Entry {login} not found, exiting...") and sys.exit(1)
    if not gpg.is_valid_passphrase(passphrase): print("Invalid passphrase, exiting...") and sys.exit(1)

    with open(get_entry_path(login), "r") as f:
        password = gpg.decrypt(
            message=f.read(),
            passphrase=passphrase
        )
        print(f"Login: {login}\nPassword: {password}")
    ...

@app.command()
def remove(login: str):
    """
    Remove existing passwords from vault
    """
    if not entry_exists(login): print(f"Entry {login} not found, exiting...") and sys.exit(1)
    confirmation = input(f"Are you sure you want to remove the {login} entry? [y/N]: ")
    if confirmation.lower() == "y":
        os.remove(get_entry_path(login))
    ...

@app.command()
def generate(login: str, length: int = 16):
    """
    Generate new login to vault
    """
    ...

@app.command()
def list(login: str):
    """
    List all passwords from vault
    """
    ...

if __name__ == "__main__":
    app()