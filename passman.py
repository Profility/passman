import os
import gnupg
import typer
import string
import errors
import secrets
from typing import List
from pathlib import Path
from typing_extensions import Annotated

HOME_DIR = os.path.expanduser("~")
PASSMAN_DIR = os.path.join(HOME_DIR, ".passman")
GPG_ID = os.path.join(PASSMAN_DIR, ".gpg_id")

gpg = gnupg.GPG()
app = typer.Typer()

def get_entry_path(entry) -> bool:
    """
    Get login entry path
    """
    return os.path.join(PASSMAN_DIR, entry+".gpg")

def entry_exists(entry) -> bool:
    """
    Returns if login entry exists
    """
    return os.path.exists(get_entry_path(entry))

def get_gpg_id() -> List[str]:
    """
    Returns all GPG Ids within .gpg_id file
    """
    if not os.path.exists(GPG_ID): errors.GPGIdNotFound()
    with open(GPG_ID, "r") as f:
        return f.read().splitlines()
    
def is_initialized() -> bool:
    """
    Returns if vault is initialized
    """
    return os.path.exists(PASSMAN_DIR) and os.path.exists(os.path.join(PASSMAN_DIR, ".gpg_id"))

def create_entry(login, password, gpg_id):
    """
    Creates a new entry
    """
    if "/" in login:
        login_path = login.split("/")
        if len(login_path) == 2:
            folder = os.path.join(PASSMAN_DIR, login_path[0])
            if not os.path.exists(folder): os.makedirs(folder)

    gpg.encrypt(
        data=password,
        recipients=gpg_id,
        output=os.path.join(PASSMAN_DIR, login+".gpg")
    )

def get_entry(login):
    password = gpg.decrypt_file(get_entry_path(login))
    if not password.ok: errors.DecryptionError(password.status)

    return password

@app.command()
def init(gpg_id: List[Path]):
    """
    Initializes PassMan vault
    """

    ids = [id.name for id in gpg_id]
    if not os.path.exists(PASSMAN_DIR): os.makedirs(PASSMAN_DIR)

    with open(os.path.join(PASSMAN_DIR, ".gpg_id"), "w") as f:
        for id in ids:
            f.write(id + "\n")

    print(f"Vault initialized for {' '.join(ids)}, it can be found at {PASSMAN_DIR}")

@app.command()
def insert(
    login: str,
    password: Annotated[str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)]):
    """
    Add existing passwords to vault
    """

    gpg_id = get_gpg_id()
    entry = get_entry_path(login)

    if entry_exists(login): errors.EntryAlreadyExists(login)

    create_entry(login, password, gpg_id)

    print("Added existing password at ", entry)

@app.command()
def generate(
    login: str,
    length: Annotated[int, typer.Argument()] = 16):
    """
    Generate new login to vault
    """
    entry = get_entry_path(login)

    if entry_exists(login): errors.EntryAlreadyExists(login)
    
    gpg_id = get_gpg_id()
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))

    create_entry(login, password, gpg_id)
    print(f"The generated password for {entry} is {password}")

@app.command()
def view(login: str):
    """
    View specific login from vault
    """
    if not is_initialized(): errors.NotInitialized()
    if not entry_exists(login): errors.EntryNotFound(login)

    password = get_entry(login)
    
    print(f"Login: {login}\nPassword: {password.data.decode()}")

@app.command()
def remove(login: str):
    """
    Remove existing passwords from vault
    """
    if not is_initialized(): errors.NotInitialized()
    if not entry_exists(login): errors.EntryNotFound(login)

    errors.EntryAlreadyExists(login)

    os.remove(get_entry_path(login))
    print(f"Removed {login} entry")

@app.command()
def list():
    """
    List all passwords from vault
    """
    if not is_initialized(): errors.NotInitialized()

    for item in os.listdir(PASSMAN_DIR):
        current_item = os.path.join(PASSMAN_DIR, item)
        if os.path.isdir(current_item):
            print(item)
            for sub_item in os.listdir(current_item):
                print(f"└── {sub_item}")
        elif os.path.isfile(current_item) and item.endswith(".gpg"):
            print(item)

if __name__ == "__main__":
    app()