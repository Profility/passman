from . import errors
import gnupg
import os
from pathlib import Path
from typing import List

gpg = gnupg.GPG()

HOME_DIR = os.path.expanduser("~")
PASSMAN_DIR = os.path.join(HOME_DIR, ".passman")
GPG_ID = os.path.join(PASSMAN_DIR, ".gpg_id")

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