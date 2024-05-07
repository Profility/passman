# PassMan
**PassMan** is a terminal password manager written in Python, heavily inspired by [pass](https://www.passwordstore.org/)

You interact with PassMan from the terminal, give it a password and it encrypts it with GPG and gets stored locally safely in your computer, you decrypt it with your GPG passphrase, simple enough right?

## Dependencies:
- [GNUPG](https://gnupg.org/download/index.html) - used for encrypting & decrypting your passwords
- [typer](https://typer.tiangolo.com/) - used for the CLI interface

## Usage:
Start by initializing the passman vault by running `py passman.py init`
```
PS C:\Users\Marcus> > py passman.py init [gpg key ID]
Vault initialized for [gpg key ID], it can be found C\Users\Marcus\.passman
```

And you are set in using passman! Run `py passman.py --help` for information 
about the commands you can use!


## To-Do:
- [ ] Add folder support for entries
- [ ] Prettify interface
- [ ] Make it a package
- [ ] Add metadata support
- [x] Improve 'init' command and handling IDs
- [x] Implement 'generate' and 'list' command
- [x] Error handling class