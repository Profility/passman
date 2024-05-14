# PassMan
**PassMan** is a terminal password manager written in Python, heavily inspired by [pass](https://www.passwordstore.org/)

You interact with PassMan from the terminal, give it a password and it encrypts it with GPG and gets stored locally safely in your computer, you decrypt it with your GPG passphrase, simple enough right?

You can install **PassMan** by running:
`pip install python-passman`

## Dependencies:
- [python-gnupg](https://docs.red-dove.com/python-gnupg/) - interacting with GnuPG
- [typer](https://typer.tiangolo.com/) - used for the command-line interface

## Usage:
Start by initializing the passman vault by running `passman init [gpg key ID]`
```
passman init [ID]
Vault initialized for [ID], it can be found at [path]
```

And you are set in using passman! Run `passman --help` for information 
about the commands you can use!


## To-Do:
- [ ] Using vim or nano when editing
- [x] Make it a package
- [x] Prettify interface
- [x] 'List' cmd shows nested folders/files
- [x] Add metadata support
- [x] Add folder support for entries
- [x] Improve 'init' command and handling IDs
- [x] Implement 'generate' and 'list' command
- [x] Error handling class