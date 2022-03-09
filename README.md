# nyanpass

## Nyanpass: Yet Another New Password-generation And Strength-calculation Script

A strong, flexible password generator written in Python. Use it for whatever.

## Features

* Choose from any combination of character sets including lowercase, uppercase,
digits, punctuation, space, hexadecimal, base64, hiragana, katakana and jouyou
kanji
* Measures generated password strength in bits of information entropy and
describes its resistance to brute force attack in real-world terms
* Specify either a password length in characters, or a minimum password strength
in bits
* `quiet` mode for piping the password to other programs, `verbose` for more
information
* Uses `random.SystemRandom()` for good randomness

## Usage

`python nyanpass.py 20 chars lower upper digits`

## Help

* `python nyanpass.py help`
* `python nyanpass.py very help`

## Changes

* See [CHANGELOG](CHANGELOG.md).

## Disclaimer

I'm not a cryptographer. However, the documentation for the Python module
[secrets](https://docs.python.org/3/library/secrets.html) promises that it's
suitable for for generating cryptographically strong passwords.
