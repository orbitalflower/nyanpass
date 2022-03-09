# Changelog

v1.0 --- 13 May 2015

* Initial release
* Randomly chooses passwords based on a user-defined character set, and either a
password length or minimum password strength measured in bits of information
entropy
* Verbose mode shows interesting information about password strength

v2.0 --- 23 Oct 2015

* New user-friendly syntax. No longer uses dash notation, breaks compatibility
with old version. Drops argparse.
* Various option changes. `terse` is now `quiet`. A few abbreviations changed or
were removed because reasons. Many new aliases for convenience (e.g. both "hex"
and "hexadecimal" will work now). New character set groups (e.g. alnum, letters,
japanese).
* New preset mode for generating wi-fi passwords. New character set groups
* New modes for morse code, `morse` and `morse64` (base64 but with dots and
dashes). Useful to add two easily-typed punctuation characters
* Tidier verbose output.
* Now easier to import as a module into other programs.

v2.1 --- 2 May 2016

* Forgot to upload this one
* Update to Python 3
* Make char length the default specifier
* Allow "digit" specifier

v2.2 --- 9 Mar 2021

* Switched from random.SystemRandom().choice() to secrets.choice().
* Changed the word "unbreakable" to "unbruteforceable".
* Allow "word" specifier
* Recommend DuckDuckGo for unimplemented "word" mode.
