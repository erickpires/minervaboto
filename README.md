# Description

This is a renew tool for the UFRJ library system.

# Usage
For now we have three ways to get login credentials.

## Via environment variables:
This is the default way. If you run `minervaboto` with no arguments it will search
for MINERVA_ID and MINERVA_PASS environment variables and use then for _id_ and
_password_ respectively.

## Via a config file:
Just run `minervaboto --config`. The _id_ and _password_ are gonna be read from a config
file in the appropriate directory on your system. When you use this mode with an empty
config file (e.g. when you are running for the first time) it will prompt you the
credentials and write then to the file.

## Via program arguments:
You can pass the credentials directly by running `minervaboto <id> <password>`.

# Installation
The easiest way to install `minervaboto` is to run `pip install minervaboto`.

If you are using Arch Linux, there's also the [`python-minervaboto`](https://aur.archlinux.org/packages/python-minervaboto/) AUR package.

You can also clone the repository and run `python setup.py install`.
