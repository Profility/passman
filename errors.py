import sys

class PassManError(Exception):
    def __init__(self, message):
        print(message)
        sys.exit(1)

class PassManConfirmation():
    def __init__(self, message):
        confirmation = input(f"{message} [y/N]: ")
        if confirmation.lower() == "n":
            sys.exit(0)

def NotInitialized():
    """If passman vault is not yet initialized"""

    PassManError("Passman vault not initialized, please run `passman init`")

def EntryNotFound(entry):
    """If login entry is not found"""

    PassManError(f"Entry '{entry}' not found, exiting...")

def GPGIdNotFound():
    """If GPG Id is not found"""

    PassManError("GPG ID file does not exist, please run `passman init`")\
    
def EntryAlreadyExists(entry):
    """If login entry already exists"""

    PassManConfirmation(f"Entry '{entry}' already exists, overwrite?")

def DecryptionError(status):
    """If decryption fails"""

    PassManError(f"Decryption failed; {status}, exiting...")