# nyanpass

## Nyanpass, Yet Another New Password-generation And Strength-calculation Script

A strong, flexible password generator written in Python.

## Features

* Choose from any combination of character sets including lowercase, uppwercase,
digits, punctuation, space, hexadecimal, base64, hiragana, katakana and jouyou
kanji
* Measures generated password strength in bits of information entropy and
describes its resistance to brute force attack in real-world terms
* Specify either a maximum password length or minimum password strength
* `--terse` mode for piping the password to other programs, `--verbose` for
more information (default)
* Uses `random.SystemRandom()`

## Usage

`python nyanpass.py [-abdijklpsux] [-c LENGTH | -e ENTROPY] [--terse|--verbose]
[--help | --very-help]`

### Examples

* `python nyanpass.py` --- Generate very strong 128-bit password including
lowercase, uppercase, digits and punctuation
* `python nyanpass.py -l -c 16` --- Generate moderately strong 16-character
all-lowercase password for ease of typing on a smartphone
* `python nyanpass.py -e 256` --- Read Bruce Schneier's advice on why anything
over 256 bits is excessive
