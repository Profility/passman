import os
import gnupg
import typer
import string
import errors
import secrets
import tempfile
import subprocess
from typing import List
from pathlib import Path
from typing_extensions import Annotated

HOME_DIR = os.path.expanduser("~")
PASSMAN_DIR = os.path.join(HOME_DIR, ".passman")
GPG_ID = os.path.join(PASSMAN_DIR, ".gpg_id")

gpg = gnupg.GPG()
app = typer.Typer()

class PassMan:
    @staticmethod
    def get_entry_path(entry: str) -> str:
        """Get login entry path"""

        return os.path.join(PASSMAN_DIR, entry+".gpg")

    @staticmethod
    def entry_exists(entry: str) -> bool:
        """Returns if login entry exists"""

        return os.path.exists(PassMan.get_entry_path(entry))
    
    @staticmethod
    def get_file_content(file: Path) -> str:
        """Returns file contents"""
        with open(file, "r") as f:
            return f.read()

    @staticmethod
    def get_gpg_id() -> List[str]:
        """Returns all GPG Ids within .gpg_id file"""

        if not os.path.exists(GPG_ID): 
            raise errors.GPGIdNotFound()
        
        return PassMan.get_file_content(GPG_ID).splitlines()
        
    @staticmethod
    def is_initialized() -> bool:
        """Returns if vault is initialized"""

        return os.path.exists(PASSMAN_DIR) and os.path.exists(os.path.join(PASSMAN_DIR, ".gpg_id"))

    @staticmethod
    def create_entry(login: str, password: str, gpg_id: List[str]):
        """Creates a new entry"""

        if "/" in login:
            folders = os.path.join(PASSMAN_DIR, os.path.dirname(login))
            if not os.path.exists(folders):
                os.makedirs((folders), exist_ok=True)

        gpg.encrypt(
            data=password,
            recipients=gpg_id,
            output=os.path.join(PASSMAN_DIR, login+".gpg")
        )

    @staticmethod
    def get_entry(login: str):
        password = gpg.decrypt_file(PassMan.get_entry_path(login))
        if not password.ok: 
            raise errors.DecryptionError(password.status)

        return password

@app.command()
def init(gpg_id: List[Path]):
    """Initializes PassMan vault"""

    ids = [id.name for id in gpg_id]
    if not os.path.exists(PASSMAN_DIR): 
        os.makedirs(PASSMAN_DIR)

    with open(os.path.join(PASSMAN_DIR, ".gpg_id"), "w") as f:
        for id in ids:
            f.write(id + "\n")

    print(f"Vault initialized for {' '.join(ids)}, it can be found at {PASSMAN_DIR}")

@app.command()
def add(
    login: str,
    password: Annotated[str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)]):
    """Add existing passwords to vault"""

    gpg_id = PassMan.get_gpg_id()
    entry = PassMan.get_entry_path(login)

    if PassMan.entry_exists(login):
        errors.EntryAlreadyExists(login)

    PassMan.create_entry(login, password, gpg_id)

    print("Added existing password at ", entry)

@app.command()
def generate(
    login: str,
    length: Annotated[int, typer.Argument()] = 16):
    """Generate new login to vault"""

    entry = PassMan.get_entry_path(login)

    if PassMan.entry_exists(login): 
        errors.EntryAlreadyExists(login)
    
    gpg_id = PassMan.get_gpg_id()
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))

    PassMan.create_entry(login, password, gpg_id)
    print(f"The generated password for {entry} is {password}")

@app.command()
def view(login: str):
    """View specific login from vault"""

    if not PassMan.is_initialized(): 
        raise errors.NotInitialized()
    if not PassMan.entry_exists(login): 
        raise errors.EntryNotFound(login)

    password = PassMan.get_entry(login)
    
    print(f"Login: {login}\nPassword: {password.data.decode()}")

@app.command()
def rm(login: str):
    """Remove existing passwords from vault"""

    if not PassMan.is_initialized(): 
        raise errors.NotInitialized()
    if not PassMan.entry_exists(login): 
        raise errors.EntryNotFound(login)

    os.remove(PassMan.get_entry_path(login))
    print(f"Removed {login} entry")

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

        print(f"Edited {login} entry")
    finally:
        os.remove(changes_file.name)

@app.command()
def ls():
    """List all passwords from vault"""

    if not PassMan.is_initialized(): 
        errors.NotInitialized()

    for root, dirs, files in os.walk(PASSMAN_DIR):
        indent_level = root.replace(PASSMAN_DIR, "").count(os.sep)
        indentation = " " * 2 * indent_level
        base_root_name = os.path.basename(root)

        if indent_level < 2:
            if not base_root_name == ".passman":
                print(f'[{base_root_name}]')
        else:
            print(f'{indentation}[{base_root_name}]')

        for file in files:
            if not file == ".gpg_id" and file.endswith(".gpg"): 
                print(f'{indentation} => {os.path.basename(file).split(".gpg")[0]}')

if __name__ == "__main__":
    app()