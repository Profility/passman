import sys

class PassManError(Exception):
    def __init__(self, message):
        print(message)
        sys.exit(1)

def NotInitialized():
    """If passman vault is not yet initialized"""

    PassManError("Passman vault not initialized, please run `passman init`")

def AlreadyInitialized():
    """If passman vault is already initialized"""

    PassManError("Passman vault already initialized, exiting...")

def EntryNotFound(entry):
    """If login entry is not found"""

    PassManError(f"Entry {entry} not found, exiting...")

def GPGIdNotFound():
    """If GPG Id is not found"""

    PassManError("GPG ID file does not exist, please run `passman init`")