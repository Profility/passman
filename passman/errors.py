from rich import print
from rich.prompt import Confirm
import sys

class PassManError(Exception):
    def __init__(self, message):
        print(message)
        sys.exit(1)

class PassManConfirmation():
    def __init__(self, message):
        confirmation = Confirm.ask(message)
        if not confirmation:
            sys.exit(0)

def NotInitialized():
    """If passman vault is not yet initialized"""

    PassManError("Passman vault [bold red]not initialized[/], please run [bold]`passman init`[/]")

def EntryNotFound(entry):
    """If login entry is not found"""

    PassManError(f"Entry '{entry}' [bold red]not found[/], exiting...")

def GPGIdNotFound():
    """If GPG Id is not found"""

    PassManError("GPG ID file does [bold red]not exist[/], please run [bold]`passman init`[/]")
    
def EntryAlreadyExists(entry):
    """If login entry already exists"""

    PassManConfirmation(f"Entry '{entry}' [bold red]already exists[/], overwrite?")

def PasswordsDontMatch():
    """If passwords don't match"""

    PassManError("Passwords [bold red]don't match[/], exiting...")

def DecryptionError(status):
    """If decryption fails"""

    PassManError(f"Decryption failed; [bold red]{status}[/], exiting...")