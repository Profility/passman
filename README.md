# PassMan - A password manager 

![GitHub License](https://img.shields.io/github/license/profility/passman) ![PyPI - Version](https://img.shields.io/pypi/v/python-passman)

**PassMan** is a terminal password manager written in Python. Helps you securely store secrets locally within gpg encrypted files and easily manage them, heavily inspired by [pass](https://www.passwordstore.org/)

`pip install python-passman`

### Setting Up:
Make sure you have an existing GPG-keypair. If not, run: 
```
gpg --full-generate-key
```
Follow along the instructions and copy the ID of your GPG-key.

```
passman init [gpg-id]
Vault initialized for [gpg-id], it can be found at [home_dir]
```
Here, we initialize the `.passman` vault, where all your secrets will be stored in.

And you are all set! Run `passman --help` to get all the commands you can run:
```
Usage: passman [OPTIONS] COMMAND [ARGS]...

Commands
add         Add existing passwords to vault
edit        Edit specific entry content
generate    Generate new login to vault
init        Initializes PassMan vault
ls          List all passwords from vault
rm          Remove existing password from vault
view        View specific login from vault
```

### Dependencies:
- [GnuPG](https://gnupg.org/) - for encrypting/decrypting secrets
- [typer](https://typer.tiangolo.com/) - for the command-line interface
- [python-gnupg](https://docs.red-dove.com/python-gnupg/) - accessing GnuPG