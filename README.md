# PassMan
**PassMan** is a terminal password manager written in Python, heavily inspired by [pass](https://www.passwordstore.org/)

You interact with PassMan from the terminal, give it a password and it encrypts it with GPG and gets stored locally safely in your computer, you decrypt it with your GPG passphrase, simple enough right?

## Dependencies:
You can install the dependencies by running `pip install -r requirements.txt`
- [python-gnupg](https://docs.red-dove.com/python-gnupg/) - interacting with GnuPG
- [typer](https://typer.tiangolo.com/) - used for the command-line interface

## Usage:
Start by initializing the passman vault by running `py passman.py init [gpg key ID]`
```
PS C:\Users\Marcus> > py passman.py init [gpg key ID]
Vault initialized for [gpg key ID], it can be found C\Users\Marcus\.passman
```

And you are set in using passman! Run `py passman.py --help` for information 
about the commands you can use!


## To-Do:
- [ ] Using vim or nano when editing
- [ ] Prettify interface
- [ ] Make it a package
- [x] 'List' cmd shows nested folders/files
- [x] Add metadata support
- [x] Add folder support for entries
- [x] Improve 'init' command and handling IDs
- [x] Implement 'generate' and 'list' command
- [x] Error handling class