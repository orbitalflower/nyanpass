#!/usr/bin/env python

import random, string, sys
from math import log, ceil
from textwrap import fill, wrap

"""
  nyanpass.py
  Randomly generates a strong password.
"""

# Meta
VERSION = "2.0"

# Defaults
DEFAULT_VERBOSITY = True
DEFAULT_CHARSET = {"lowercase", "digits"}
DEFAULT_MODE = "bit" # perhaps change this to "word" in future
DEFAULT_LENGTH = {"char": 28, "word": 4, "bit": 128, "byte": 16, "help": 0,
  "very-help": 0, "wpa": 40, "wep": 26}

# Supported charsets, including aliases
SUPPORTED_CHARSETS = ["all", "alphabetic", "alphanumeric", "alnum", "b64",
  "base64", "d", "digits", "h", "hex", "hiragana", "j", "japanese", "k",
  "kanji", "hexadecimal", "katakana", "l", "letters", "lower", "lowercase",
  "m", "morse", "morsecode", "code", "m64", "morse64", "numbers", "numeric",
  "n", "p", "punctuation", "s", "space", "spaces", "strong", "symbols", "u",
  "upper", "uppercase", "x"]

def main():
  # Parse input
  cs = set()
  mode = ""
  length = 0
  verbose = DEFAULT_VERBOSITY

  for arg in sys.argv[1:]:
    if arg in SUPPORTED_CHARSETS:
      cs.update(charset_by_alias(arg))
    elif arg in ["bits", "bit", "b"]:
      mode = "bit"
    elif arg in ["bytes", "byte", "B"]:
      mode = "byte"
    elif arg in ["words", "words", "xkcd", "xkcdpass", "diceware", "w"]:
      mode = "word"
    elif arg in ["chars", "char", "chr", "chrs", "c", "characters", "length", "len", "long"]:
      mode = "char"
    elif arg in ["very-help", "very", "--very-help", "-H"]:
      mode = "very-help"
    elif arg in ["help", "-h", "--help"]:
      if mode in ["very-help", "help"]:
        mode = "very-help"
      else:
        mode = "help"
    elif arg in ["wifi", "wi-fi", "WIFI", "WI-FI", "WPA", "WPA2", "wpa2", "wpa"]:
      mode = "wpa"
    elif arg in ["WEP", "wep"]:
      mode = "wep"
    elif arg.isdigit():
      length = int(arg)
    elif arg in ["verbose", "--verbose", "-v"]:
      verbose = True
    elif arg in ["quiet", "--quiet", "terse", "--terse", "-q", "-t"]:
      verbose = False
    else:
      for char in arg:
        if char in SUPPORTED_CHARSETS:
          cs.update(charset_by_alias(char))
        else:
          show_help("ERROR: Unknown argument {}.".format(arg))

  # Help first
  if mode == "help":
    show_help()
  elif mode == "very-help":
    show_extra_information("very-help")

  # Set defaults
  if mode == "":
    mode = DEFAULT_MODE
  if len(cs) < 1:
    cs = DEFAULT_CHARSET
  if length < 1:
    length = DEFAULT_LENGTH[mode]
  if verbose == None:
    verbose = DEFAULT_VERBOSITY

  # Generate password
  if mode in ["bit", "byte", "char"]:
    generate_password(mode, cs, length, verbose)
  elif mode == "word":
    show_help("OOPS: Word mode not implemented yet.")
  elif mode == "wpa":
    generate_password("char", {"lowercase", "digits"}, length, verbose)
    show_extra_information("wpa")
  elif mode == "wep":
    generate_password("char", {"hex"}, length, False)
    show_extra_information("wep")

  exit()

def charset_by_alias(arg):
  csets = []
  if arg in ["u", "upper", "uppercase"] or arg in ["letters", "alphabetic",
    "alphanumeric", "alnum", "all", "strong", "morse64", "m64"]:
    csets.append("uppercase")
  if arg in ["l","lower", "lowercase"] or arg in ["letters", "alphabetic",
    "alphanumeric", "alnum", "all", "strong", "morse64", "m64"]:
    csets.append("lowercase")
  if arg in ["d","digits", "numbers", "number", "digit", "numeric",
    "n"] or arg in ["alphanumeric", "alnum", "all", "strong", "morse64", "m64"]:
    csets.append("digits")
  if arg in ["base64", "b64"]:
    csets.append("base64")
  if arg in ["p", "punctuation", "symbols", "symbol",
    "special"] or arg in ["all", "strong"]:
    csets.append("punctuation")
  if arg in ["s", "space", "spaces"]:
    csets.append("space")
  if arg in ["m", "morse", "morsecode", "code", "morse64", "m64"]:
    csets.append("morse code")
  if arg in ["x", "hex", "hexadecimal"]:
    csets.append("hex")
  if arg in ["j", "kanji"] or arg in ["japanese"]:
    csets.append("kanji")
  if arg in ["h", "hiragana"] or arg in ["japanese"]:
    csets.append("hiragana")
  if arg in ["k", "katakana"] or arg in ["japanese"]:
    csets.append("katakana")

  return csets
    
def show_help(msg=None):
  if msg:
    print msg

  print "Nyanpass {}, a strong password generator.".format(VERSION)

  print """Usage: nyanpass.py [<N> chars|bits] [CHARSET...] [OPTIONS...]

 Example:
  nyanpass.py 16 chars lowercase uppercase digits

 Character sets (choose one or more):
  uppercase, lowercase, digits, punctuation, space, base64, hex, kanji,
  katakana, hiragana, japanese, letters, all, strong

 Options:
  verbose     Shows interesting information about password strength{}
  quiet       Output only the password{}
  help        This help
  very help   Extended help, extra modes, abbreviations""".format(
    " (default)"*DEFAULT_VERBOSITY, " (default)"*(not DEFAULT_VERBOSITY))

  exit()

def cat_charsets(cs):
  """Combine a set into an alphabetically sorted list in written English,
  using commas and 'and'. """
  d = sorted(cs)
  if len(d) > 2:
    d[-1] = "and " + d[-1]
    d = string.join(d, ", ")
  else:
    d = string.join(d, " and ")
  return d

def show_extra_information(msg):
  d = cat_charsets(DEFAULT_CHARSET)

  messages = {}
  messages["very-help"] = """Nyanpass {}, a strong password generator.

SPECIAL OPTIONS
 nyanpass.py wpa
  Generates a strong password for a wi-fi network.

 nyanpass.py wep
  Try this if you're still on a WEP network.

CHARACTER SETS
 You can use one or more character sets. Most character sets have a single
 letter abbreviation and various aliases for convenience.

 u, upper, uppercase       ABCDEFGHIJKLMNOPQRSTUVWXYZ
 l, lower, lowercase       abcdefghijklmnopqrstuvwzyz
 d, n, digits, numbers     0123456789
 x, hex, hexadecimal       0123456789abcdef
 p, punctuation, symbols   '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{}~'
 s, space                  Space character
 m, morse, morsecode       Dots and dashes
 h, hiragana               Japanese hiragana
 k, katakana               Japanese katakana
 j, kanji                  Japanese jouyou kanji

 There are also several combined groups, for convenience:

 letters, alphabetic       Uppercase and lowercase
 alphanumeric, alnum       Uppercase, lowercase, and digits
 b64, base64               Uppercase, lowercase, digits, + and /
 m64, morse64              Uppercase, lowercase, digits, . and -
 all, strong               Uppercase, lowercase, digits and punctuation
 japanese                  Hiragana, katakana and kanji

MODES
 Character mode (e.g. nyanpass.py 16 chars)
  Generates a password with exactly the requested number of characters.

 Bit mode (e.g. nyanpass.py 128 bits)
  Generates a password with at least the requested number of bits entropy,
  a reliable measure of randomly generated password strength. Can also
  specify in bytes.

 Word mode (e.g. nyanpass.py 4 words)
  Not yet implemented.

OPTIONS
 verbose     Gives interesting information on the strength of your password.
             Spaces the password out into groups of four characters for
             readbility, unless the chosen character set contains spaces.{}
 quiet       Output only the password. Useful to pipe into another program.{}
 help        That help.
 very help   This help.

DEFAULTS
 If no parameters are supplied, Nyanpass generates a {} {} password
 from {}.

ADVICE
 You should choose a password with at least 64 bit strength, preferably 96
 bits. More than 128 bit is overkill, and more than 256 bit is ridiculous. 40
 bits or lower is too weak nowadays.

 Remember one good password and use it to guard your main e-mail account,
 along with two-factor authentication. Protect your other accounts with strong
 passwords which you keep in a password manager of some sort.

 A strong password is not a substitute for good security posture. Stay on top
 of operating system updates and do not download software from unreliable
 sources or sites without HTTPS.

USEFUL SETTINGS
 128 bit all: Fits in most password fields (20 chars), very strong.
 128 bit lowercase: Longer (26 characters), but useful on sites that forbid
  special characters, and easier to type on mobile devices.
 128 bit japanese: Shorter (12 characters), requires sites that support unicode
  passwords, but rare for an attacker to try to brute force.
 80 bit alphanumeric: Easy to type into a smartphone lock screen with a
  16-character limit, but still quite secure and reasonably easy to remember
  with practice.
 75 bit alphabetic: Quicker to type, 16 character limit, still quite secure.

AMUSING SETTINGS
 1 char kanji: Flash card mode!
 5 char lowercase: See how fast they can break John Oliver's password.
 256 bit / 224 bit / 192 bit: Bruce Schneier quotes on why more than 128 bits
  is unnecessary.

SECURITY
 Human-selected passwords tend to fall into highly predictable patterns and are
 not as secure as they appear. Machine-generated passwords are more random.

 This program generates passwords with random.SystemRandom().choice(charset),
 which is believed to be sufficiently random to generate strong passwords.

 Where two or more character sets contain the same characters, each appears
 only once in the set used by the random generator, and is evenly likely to
 be chosen.

BUGS
 no

LICENSE
 This is free and unencumbered software released into the public domain.""".format(VERSION,
  "{|}", "\n             Enabled by default."*DEFAULT_VERBOSITY,
  "\n             Enabled by default."*(not DEFAULT_VERBOSITY),
  DEFAULT_LENGTH[DEFAULT_MODE], DEFAULT_MODE, d)

  messages["wpa"] = """
A password of 128 bit strength or more is recommended for wi-fi. The default
password supplied with a home router is frequently not sufficient.

You should change your wi-fi password at least occasionally. For ease of typing
into mobile devices, this password has been selected using only lowercase and
digits, with sufficient length to resist attack."""

  messages["wep"] = """==================== STOP ====================
WEP is no longer considered secure for any strength of password. An attacker
can break WEP in seconds. Switch your device to WPA or WPA2 immediately and
generate a new WPA key."""

  if msg in ["very-help", "wpa", "wep"]:
    print messages[msg]
    exit()

def generate_password(mode=DEFAULT_MODE, charsets=DEFAULT_CHARSET,
  length=DEFAULT_LENGTH[DEFAULT_MODE], verbose=False):
  """ Randomly generate a password:
  mode: bit, byte, char or word. Specifies what units the password length
    is measured in.
  charsets: Set of named character sets used in the password.
    See SUPPORTED_CHARSETS.
  length: Length of password as an integer.
  verbose: If true, outputs interesting data. Otherwise, only outputs the
    password."""
  space_forbidden = False
  charset = ""
  for cs in charsets:
    if cs == "uppercase":
      charset += string.uppercase
    elif cs == "lowercase":
      charset += string.lowercase
    elif cs == "digits":
      charset += string.digits
    elif cs == "punctuation":
      charset += string.punctuation
    elif cs == "space":
      charset += " "
      space_forbidden = True
    elif cs == "base64":
      charset += string.letters + string.digits + "+/"
    elif cs == "morse code":
      charset += ".-"
    elif cs == "hex":
      charset += "0123456789ABCDEF"
# Interestingly, string.hexdigits isn't suitable here because it contains both
# uppercase and lowercase letters, thus making letters twice as likely to
# appear.
    elif cs == "hiragana":
      charset += u'\u3042\u3044\u3046\u3048\u304a\u304b\u304d\u304f\u3051\u3053\u3055\u3057\u3059\u305b\u305d\u305f\u3061\u3064\u3066\u3068\u306a\u306b\u306c\u306d\u306e\u306f\u3072\u3075\u3078\u307b\u307e\u307f\u3080\u3081\u3082\u3089\u308a\u308b\u308c\u308d\u308f\u3092\u3093\u304c\u304e\u3050\u3052\u3054\u3056\u3058\u305a\u305c\u305e\u3060\u3062\u3065\u3067\u3069\u3070\u3073\u3076\u3079\u307c\u3071\u3074\u3077\u307a\u307d\u3084\u3086\u3088'
    elif cs == "katakana":
      charset += u'\u30a2\u30a4\u30a6\u30a8\u30aa\u30ab\u30ad\u30af\u30b1\u30b3\u30b5\u30b7\u30b9\u30bb\u30bd\u30bf\u30c1\u30c4\u30c6\u30c8\u30ca\u30cb\u30cc\u30cd\u30ce\u30cf\u30d2\u30d5\u30d8\u30db\u30de\u30df\u30e0\u30e1\u30e2\u30e9\u30ea\u30eb\u30ec\u30ed\u30ac\u30ae\u30b0\u30b2\u30b4\u30b6\u30b8\u30ba\u30bc\u30be\u30c0\u30c2\u30c5\u30c7\u30c9\u30d0\u30d3\u30d6\u30d9\u30dc\u30d1\u30d4\u30d7\u30da\u30dd\u30e3\u30e5\u30e7\u30ef\u30f2\u30f3'
    elif cs == "kanji":
      charset += u'\u4e9e\u54c0\u6328\u611b\u66d6\u60e1\u63e1'
      charset += u'\u58d3\u6271\u5b9b\u5d50\u5b89\u6848\u6697\u4ee5\u8863\u4f4d'
      charset += u'\u570d\u91ab\u4f9d\u59d4\u5a01\u7232\u754f\u80c3\u5c09\u7570'
      charset += u'\u79fb\u840e\u5049\u6905\u5f59\u610f\u9055\u7dad\u6170\u907a'
      charset += u'\u7def\u57df\u80b2\u4e00\u58f9\u9038\u8328\u828b\u5f15\u5370'
      charset += u'\u56e0\u54bd\u59fb\u54e1\u9662\u6deb\u9670\u98f2\u96b1\u97fb'
      charset += u'\u53f3\u5b87\u7fbd\u96e8\u5504\u9b31\u755d\u6d66\u904b\u96f2'
      charset += u'\u6c38\u6cf3\u82f1\u6620\u69ae\u71df\u8a60\u5f71\u92ed\u885e'
      charset += u'\u6613\u75ab\u76ca\u6db2\u9a5b\u60a6\u8d8a\u8b01\u95b2\u5713'
      charset += u'\u5ef6\u6cbf\u708e\u6028\u5bb4\u5a9b\u63f4\u5712\u7159\u733f'
      charset += u'\u9060\u925b\u9e7d\u6f14\u7de3\u8277\u6c5a\u738b\u51f9\u592e'
      charset += u'\u61c9\u5f80\u62bc\u65fa\u6b50\u6bc6\u6afb\u7fc1\u5967\u6a6b'
      charset += u'\u5ca1\u5c4b\u5104\u61b6\u81c6\u865e\u4e59\u4ffa\u5378\u97f3'
      charset += u'\u6069\u6eab\u7a69\u4e0b\u5316\u706b\u52a0\u53ef\u5047\u4f55'
      charset += u'\u82b1\u4f73\u50f9\u679c\u6cb3\u82db\u79d1\u67b6\u590f\u5bb6'
      charset += u'\u8377\u83ef\u83d3\u8ca8\u6e26\u904e\u5ac1\u6687\u798d\u9774'
      charset += u'\u5be1\u6b4c\u7b87\u7a3c\u8ab2\u868a\u7259\u74e6\u6211\u756b'
      charset += u'\u82bd\u8cc0\u96c5\u9913\u4ecb\u56de\u7070\u6703\u5feb\u6212'
      charset += u'\u6539\u602a\u62d0\u6094\u6d77\u754c\u7686\u68b0\u7e6a\u958b'
      charset += u'\u968e\u584a\u6977\u89e3\u6f70\u58de\u61f7\u8ae7\u8c9d\u5916'
      charset += u'\u52be\u5bb3\u5d16\u6daf\u8857\u6168\u84cb\u8a72\u69ea\u9ab8'
      charset += u'\u57a3\u67ff\u5404\u89d2\u64f4\u9769\u683c\u6838\u6bbc\u90ed'
      charset += u'\u89ba\u8f03\u9694\u95a3\u78ba\u7372\u5687\u7a6b\u5b78\u5dbd'
      charset += u'\u6a02\u984d\u984e\u639b\u6f5f\u62ec\u6d3b\u559d\u6e34\u5272'
      charset += u'\u845b\u6ed1\u8910\u8f44\u4e14\u682a\u91dc\u938c\u5208\u5e72'
      charset += u'\u520a\u7518\u6c57\u7f50\u5b8c\u809d\u5b98\u51a0\u5377\u770b'
      charset += u'\u9677\u4e7e\u52d8\u60a3\u8cab\u5bd2\u559a\u582a\u63db\u6562'
      charset += u'\u68fa\u6b3e\u9593\u9591\u52f8\u5bec\u5e79\u611f\u6f22\u6163'
      charset += u'\u7ba1\u95dc\u6b61\u76e3\u7de9\u61be\u9084\u9928\u74b0\u7c21'
      charset += u'\u89c0\u97d3\u8266\u9451\u4e38\u542b\u5cb8\u5ca9\u73a9\u773c'
      charset += u'\u9811\u9854\u9858\u4f01\u4f0e\u5371\u673a\u6c23\u5c90\u5e0c'
      charset += u'\u5fcc\u6c7d\u5947\u7948\u5b63\u7d00\u8ecc\u65e2\u8a18\u8d77'
      charset += u'\u98e2\u9b3c\u6b78\u57fa\u5bc4\u898f\u9f9c\u559c\u5e7e\u63ee'
      charset += u'\u671f\u68cb\u8cb4\u68c4\u6bc0\u65d7\u5668\u757f\u8f1d\u6a5f'
      charset += u'\u9a0e\u6280\u5b9c\u50de\u6b3a\u7fa9\u7591\u5100\u6232\u64ec'
      charset += u'\u72a7\u8b70\u83ca\u5409\u55ab\u8a70\u5374\u5ba2\u811a\u9006'
      charset += u'\u8650\u4e5d\u4e45\u53ca\u5f13\u4e18\u820a\u4f11\u5438\u673d'
      charset += u'\u81fc\u6c42\u7a76\u6ce3\u6025\u7d1a\u7cfe\u5bae\u6551\u7403'
      charset += u'\u7d66\u55c5\u7aae\u725b\u53bb\u5de8\u5c45\u62d2\u64da\u64e7'
      charset += u'\u865b\u8a31\u8ddd\u9b5a\u5fa1\u6f01\u51f6\u5171\u53eb\u72c2'
      charset += u'\u4eac\u4eab\u4f9b\u5354\u6cc1\u5cfd\u633e\u72f9\u6050\u606d'
      charset += u'\u80f8\u8105\u5f37\u6559\u9115\u5883\u6a4b\u77ef\u93e1\u7af6'
      charset += u'\u97ff\u9a5a\u4ef0\u66c9\u696d\u51dd\u66f2\u5c40\u6975\u7389'
      charset += u'\u5dfe\u65a4\u5747\u8fd1\u91d1\u83cc\u52e4\u7434\u7b4b\u50c5'
      charset += u'\u7981\u7dca\u9326\u8b39\u895f\u541f\u9280\u5340\u53e5\u82e6'
      charset += u'\u9a45\u5177\u60e7\u611a\u7a7a\u5076\u9047\u9685\u4e32\u5c48'
      charset += u'\u6398\u7a9f\u718a\u7e70\u541b\u8a13\u52f3\u85b0\u8ecd\u90e1'
      charset += u'\u7fa4\u5144\u5211\u5f62\u7cfb\u5f91\u8396\u4fc2\u578b\u5951'
      charset += u'\u8a08\u60e0\u5553\u63ed\u6eaa\u7d93\u87a2\u656c\u666f\u8f15'
      charset += u'\u50be\u643a\u7e7c\u8a63\u6176\u61ac\u7a3d\u61a9\u8b66\u9dc4'
      charset += u'\u85dd\u8fce\u9be8\u9699\u5287\u64ca\u6fc0\u6841\u7f3a\u7a74'
      charset += u'\u8840\u6c7a\u7d50\u5091\u6f54\u6708\u72ac\u4ef6\u898b\u5238'
      charset += u'\u80a9\u5efa\u784f\u7e23\u5109\u517c\u528d\u62f3\u8ed2\u5065'
      charset += u'\u96aa\u5708\u5805\u6aa2\u5acc\u737b\u7d79\u9063\u6b0a\u61b2'
      charset += u'\u8ce2\u8b19\u9375\u7e6d\u986f\u9a57\u61f8\u5143\u5e7b\u7384'
      charset += u'\u8a00\u5f26\u9650\u539f\u73fe\u8237\u6e1b\u6e90\u56b4\u5df1'
      charset += u'\u6238\u53e4\u547c\u56fa\u80a1\u864e\u5b64\u5f27\u6545\u67af'
      charset += u'\u500b\u5eab\u6e56\u96c7\u8a87\u9f13\u932e\u9867\u4e94\u4e92'
      charset += u'\u5348\u5449\u5f8c\u5a2f\u609f\u7881\u8a9e\u8aa4\u8b77\u53e3'
      charset += u'\u5de5\u516c\u52fe\u5b54\u529f\u5de7\u5ee3\u7532\u4ea4\u5149'
      charset += u'\u5411\u540e\u597d\u6c5f\u8003\u884c\u5751\u5b5d\u6297\u653b'
      charset += u'\u66f4\u6548\u5e78\u62d8\u80af\u4faf\u539a\u6046\u6d2a\u7687'
      charset += u'\u7d05\u8352\u90ca\u9999\u5019\u6821\u8015\u822a\u8ca2\u964d'
      charset += u'\u9ad8\u5eb7\u63a7\u6897\u9ec3\u5589\u614c\u6e2f\u786c\u7d5e'
      charset += u'\u9805\u6e9d\u945b\u69cb\u7db1\u9175\u7a3f\u8208\u8861\u92fc'
      charset += u'\u8b1b\u8cfc\u4e5e\u865f\u5408\u62f7\u525b\u50b2\u8c6a\u514b'
      charset += u'\u544a\u8c37\u523b\u570b\u9ed1\u7a40\u9177\u7344\u9aa8\u99d2'
      charset += u'\u8fbc\u9803\u4eca\u56f0\u6606\u6068\u6839\u5a5a\u6df7\u75d5'
      charset += u'\u7d3a\u9b42\u58be\u61c7\u5de6\u4f50\u6c99\u67fb\u7802\u5506'
      charset += u'\u5dee\u8a50\u9396\u5ea7\u632b\u624d\u518d\u707d\u59bb\u91c7'
      charset += u'\u788e\u5bb0\u683d\u5f69\u63a1\u6fdf\u796d\u9f4b\u7d30\u83dc'
      charset += u'\u6700\u88c1\u50b5\u50ac\u585e\u6b73\u8f09\u969b\u57fc\u5728'
      charset += u'\u6750\u5291\u8ca1\u7f6a\u5d0e\u4f5c\u524a\u6628\u67f5\u7d22'
      charset += u'\u7b56\u9162\u643e\u932f\u54b2\u518a\u672d\u5237\u5239\u62f6'
      charset += u'\u6bba\u5bdf\u64ae\u64e6\u96dc\u76bf\u4e09\u5c71\u53c3\u68e7'
      charset += u'\u8836\u6158\u7523\u5098\u6563\u7b97\u9178\u8d0a\u6b98\u65ac'
      charset += u'\u66ab\u58eb\u5b50\u652f\u6b62\u6c0f\u4ed5\u53f2\u53f8\u56db'
      charset += u'\u5e02\u77e2\u65e8\u6b7b\u7d72\u81f3\u4f3a\u5fd7\u79c1\u4f7f'
      charset += u'\u523a\u59cb\u59c9\u679d\u7949\u80a2\u59ff\u601d\u6307\u65bd'
      charset += u'\u5e2b\u6063\u7d19\u8102\u8996\u7d2b\u8a5e\u9f52\u55e3\u8a66'
      charset += u'\u8a69\u8cc7\u98fc\u8a8c\u96cc\u646f\u8cdc\u8aee\u793a\u5b57'
      charset += u'\u5bfa\u6b21\u8033\u81ea\u4f3c\u5152\u4e8b\u4f8d\u6cbb\u6301'
      charset += u'\u6642\u6ecb\u6148\u8fad\u78c1\u990c\u74bd\u9e7f\u5f0f\u8b58'
      charset += u'\u8ef8\u4e03\U00020b9f\u5931\u5ba4\u75be\u57f7\u6fd5\u5ac9'
      charset += u'\u6f06\u8cea\u5be6\u829d\u5beb\u793e\u8eca\u820e\u8005\u5c04'
      charset += u'\u6368\u8d66\u659c\u716e\u906e\u8b1d\u90aa\u86c7\u5c3a\u501f'
      charset += u'\u914c\u91cb\u7235\u82e5\u5f31\u5bc2\u624b\u4e3b\u5b88\u6731'
      charset += u'\u53d6\u72e9\u9996\u6b8a\u73e0\u9152\u816b\u7a2e\u8da3\u58fd'
      charset += u'\u53d7\u546a\u6388\u9700\u5112\u6a39\u6536\u56da\u5dde\u821f'
      charset += u'\u79c0\u5468\u5b97\u62fe\u79cb\u81ed\u4fee\u8896\u7d42\u7f9e'
      charset += u'\u7fd2\u9031\u5c31\u8846\u96c6\u6101\u916c\u919c\u8e74\u8972'
      charset += u'\u5341\u6c41\u5145\u4f4f\u67d4\u91cd\u5f9e\u6f81\u9283\u7378'
      charset += u'\u7e31\u53d4\u795d\u5bbf\u6dd1\u8085\u7e2e\u587e\u719f\u51fa'
      charset += u'\u8ff0\u8853\u4fca\u6625\u77ac\u65ec\u5de1\u76fe\u51c6\u6b89'
      charset += u'\u7d14\u5faa\u9806\u6e96\u6f64\u9075\u8655\u521d\u6240\u66f8'
      charset += u'\u5eb6\u6691\u7f72\u7dd6\u8af8\u5973\u5982\u52a9\u5e8f\u654d'
      charset += u'\u5f90\u9664\u5c0f\u5347\u5c11\u53ec\u5320\u5e8a\u6284\u8096'
      charset += u'\u5c1a\u62db\u627f\u6607\u677e\u6cbc\u662d\u5bb5\u5c07\u6d88'
      charset += u'\u75c7\u7965\u7a31\u7b11\u5531\u5546\u6d89\u7ae0\u7d39\u8a1f'
      charset += u'\u52dd\u638c\u6676\u71d2\u7126\u785d\u7ca7\u8a54\u8b49\u8c61'
      charset += u'\u50b7\u596c\u7167\u8a73\u5f70\u969c\u61a7\u885d\u8cde\u511f'
      charset += u'\u7901\u9418\u4e0a\u4e08\u5197\u689d\u72c0\u4e58\u57ce\u6de8'
      charset += u'\u5269\u5e38\u60c5\u5834\u758a\u84b8\u7e69\u58e4\u5b43\u9320'
      charset += u'\u8b93\u91c0\u8272\u62ed\u98df\u690d\u6b96\u98fe\u89f8\u56d1'
      charset += u'\u7e54\u8077\u8fb1\u5c3b\u5fc3\u7533\u4f38\u81e3\u82af\u8eab'
      charset += u'\u8f9b\u4fb5\u4fe1\u6d25\u795e\u5507\u5a20\u632f\u6d78\u771e'
      charset += u'\u91dd\u6df1\u7d33\u9032\u68ee\u8a3a\u5be2\u613c\u65b0\u5be9'
      charset += u'\u9707\u85aa\u89aa\u4eba\u5203\u4ec1\u76e1\u8fc5\u751a\u9663'
      charset += u'\u5c0b\u814e\u9808\u5716\u6c34\u5439\u5782\u708a\u5e25\u7cb9'
      charset += u'\u8870\u63a8\u9189\u9042\u7761\u7a57\u96a8\u9ad3\u6a1e\u5d07'
      charset += u'\u6578\u636e\u6749\u88fe\u5bf8\u7028\u662f\u4e95\u4e16\u6b63'
      charset += u'\u751f\u6210\u897f\u8072\u5236\u59d3\u5f81\u6027\u9752\u9f4a'
      charset += u'\u653f\u661f\u7272\u7701\u51c4\u901d\u6e05\u76db\u5a7f\u6674'
      charset += u'\u52e2\u8056\u8aa0\u7cbe\u88fd\u8a93\u975c\u8acb\u6574\u9192'
      charset += u'\u7a0e\u5915\u65a5\u77f3\u8d64\u6614\u6790\u5e2d\u810a\u96bb'
      charset += u'\u60dc\u621a\u8cac\u8de1\u7a4d\u7e3e\u7c4d\u5207\u6298\u62d9'
      charset += u'\u7aca\u63a5\u8a2d\u96ea\u651d\u7bc0\u8aac\u820c\u7d76\u5343'
      charset += u'\u5ddd\u4ed9\u5360\u5148\u5ba3\u5c08\u6cc9\u6dfa\u6d17\u67d3'
      charset += u'\u6247\u6813\u65cb\u8239\u6230\u714e\u7fa8\u817a\u8a6e\u8e10'
      charset += u'\u7b8b\u9322\u6f5b\u7dda\u9077\u9078\u85a6\u7e96\u9bae\u5168'
      charset += u'\u524d\u5584\u7136\u79aa\u6f38\u81b3\u7e55\u72d9\u963b\u7956'
      charset += u'\u79df\u7d20\u63aa\u7c97\u7d44\u758e\u8a34\u5851\u9061\u790e'
      charset += u'\u96d9\u58ef\u65e9\u722d\u8d70\u594f\u76f8\u838a\u8349\u9001'
      charset += u'\u5009\u641c\u63d2\u6851\u5de2\u6383\u66f9\u66fe\u723d\u7a93'
      charset += u'\u5275\u55aa\u7626\u846c\u88dd\u50e7\u60f3\u5c64\u7e3d\u906d'
      charset += u'\u69fd\u8e2a\u64cd\u71e5\u971c\u9a37\u85fb\u9020\u50cf\u589e'
      charset += u'\u618e\u85cf\u8d08\u81df\u537d\u675f\u8db3\u4fc3\u5247\u606f'
      charset += u'\u6349\u901f\u5074\u6e2c\u4fd7\u65cf\u5c6c\u8cca\u7e8c\u5352'
      charset += u'\u7387\u5b58\u6751\u5b6b\u5c0a\u640d\u905c\u4ed6\u591a\u6c70'
      charset += u'\u6253\u59a5\u553e\u58ae\u60f0\u99c4\u592a\u5c0d\u9ad4\u8010'
      charset += u'\u5f85\u6020\u80ce\u9000\u5e36\u6cf0\u5806\u888b\u902e\u66ff'
      charset += u'\u8cb8\u968a\u6eef\u614b\u6234\u5927\u4ee3\u81fa\u7b2c\u984c'
      charset += u'\u7027\u5b85\u64c7\u6fa4\u5353\u62d3\u8a17\u6fef\u8afe\u6fc1'
      charset += u'\u4f46\u9054\u8131\u596a\u68da\u8ab0\u4e39\u65e6\u64d4\u55ae'
      charset += u'\u70ad\u81bd\u63a2\u6de1\u77ed\u5606\u7aef\u7dbb\u8a95\u935b'
      charset += u'\u5718\u7537\u6bb5\u65b7\u5f48\u6696\u8ac7\u58c7\u5730\u6c60'
      charset += u'\u77e5\u5024\u6065\u81f4\u9072\u7661\u7a1a\u7f6e\u7dfb\u7af9'
      charset += u'\u755c\u9010\u84c4\u7bc9\u79e9\u7a92\u8336\u7740\u5ae1\u4e2d'
      charset += u'\u4ef2\u87f2\u6c96\u5b99\u5fe0\u62bd\u6ce8\u665d\u67f1\u8877'
      charset += u'\u914e\u9444\u99d0\u8457\u8caf\u4e01\u5f14\u5ef3\u5146\u753a'
      charset += u'\u9577\u6311\u5e33\u5f35\u5f6b\u773a\u91e3\u9802\u9ce5\u671d'
      charset += u'\u8cbc\u8d85\u8178\u8df3\u5fb5\u5632\u6f6e\u6f84\u8abf\u807d'
      charset += u'\u61f2\u76f4\u6555\u6357\u6c88\u73cd\u6715\u9673\u8cc3\u93ad'
      charset += u'\u8ffd\u690e\u589c\u901a\u75db\u585a\u6f2c\u576a\u722a\u9db4'
      charset += u'\u4f4e\u5448\u5ef7\u5f1f\u5b9a\u5e95\u62b5\u90b8\u4ead\u8c9e'
      charset += u'\u5e1d\u8a02\u5ead\u905e\u505c\u5075\u5824\u63d0\u7a0b\u8247'
      charset += u'\u7de0\u8ae6\u6ce5\u7684\u7b1b\u6458\u6ef4\u9069\u6575\u6eba'
      charset += u'\u8fed\u54f2\u9435\u5fb9\u64a4\u5929\u5178\u5e97\u9ede\u5c55'
      charset += u'\u6dfb\u8f49\u5861\u7530\u50b3\u6bbf\u96fb\u6597\u5410\u59ac'
      charset += u'\u5f92\u9014\u90fd\u6e21\u5857\u8ced\u571f\u5974\u52aa\u5ea6'
      charset += u'\u6012\u5200\u51ac\u71c8\u7576\u6295\u8c46\u6771\u5230\u9003'
      charset += u'\u5012\u51cd\u5510\u5cf6\u6843\u8a0e\u900f\u9ee8\u60bc\u76dc'
      charset += u'\u9676\u5854\u642d\u68df\u6e6f\u75d8\u767b\u7b54\u7b49\u7b52'
      charset += u'\u7d71\u7a3b\u8e0f\u7cd6\u982d\u8b04\u85e4\u9b2d\u9a30\u540c'
      charset += u'\u6d1e\u80f4\u52d5\u5802\u7ae5\u9053\u50cd\u9285\u5c0e\u77b3'
      charset += u'\u5ce0\u533f\u7279\u5f97\u7763\u5fb7\u7be4\u6bd2\u7368\u8b80'
      charset += u'\u6803\u51f8\u7a81\u5c46\u5c6f\u8c5a\u9813\u8caa\u920d\u66c7'
      charset += u'\u4e3c\u90a3\u5948\u5185\u68a8\u8b0e\u934b\u5357\u8edf\u96e3'
      charset += u'\u4e8c\u5c3c\u8cb3\u5302\u8089\u8679\u65e5\u5165\u4e73\u5c3f'
      charset += u'\u4efb\u598a\u5fcd\u8a8d\u5be7\u71b1\u5e74\u5ff5\u637b\u7c98'
      charset += u'\u71c3\u60f1\u7d0d\u80fd\u8166\u8fb2\u6fc3\u628a\u6ce2\u6d3e'
      charset += u'\u7834\u9738\u99ac\u5a46\u7f75\u62dc\u676f\u80cc\u80ba\u4ff3'
      charset += u'\u914d\u6392\u6557\u5ee2\u8f29\u8ce3\u500d\u6885\u57f9\u966a'
      charset += u'\u5a92\u8cb7\u8ce0\u767d\u4f2f\u62cd\u6cca\u8feb\u525d\u8236'
      charset += u'\u535a\u8584\u9ea5\u6f20\u7e1b\u7206\u7bb1\u7bb8\u7551\u808c'
      charset += u'\u516b\u9262\u767c\u9aee\u4f10\u62d4\u7f70\u95a5\u53cd\u534a'
      charset += u'\u6c3e\u72af\u5e06\u6c4e\u4f34\u5224\u5742\u962a\u677f\u7248'
      charset += u'\u73ed\u7554\u822c\u8ca9\u6591\u98ef\u642c\u7169\u9812\u7bc4'
      charset += u'\u7e41\u85e9\u665a\u756a\u883b\u76e4\u6bd4\u76ae\u5983\u5426'
      charset += u'\u6279\u5f7c\u62ab\u80a5\u975e\u5351\u98db\u75b2\u7955\u88ab'
      charset += u'\u60b2\u6249\u8cbb\u7891\u7f77\u907f\u5c3e\u7709\u7f8e\u5099'
      charset += u'\u5fae\u9f3b\u819d\u8098\u5339\u5fc5\u6ccc\u7b46\u59eb\u767e'
      charset += u'\u6c37\u8868\u4ff5\u7968\u8a55\u6f02\u6a19\u82d7\u79d2\u75c5'
      charset += u'\u63cf\u732b\u54c1\u6ff1\u8ca7\u8cd3\u983b\u654f\u7501\u4e0d'
      charset += u'\u592b\u7236\u4ed8\u5e03\u6276\u5e9c\u6016\u961c\u9644\u8a03'
      charset += u'\u8ca0\u8d74\u6d6e\u5a66\u7b26\u5bcc\u666e\u8150\u6577\u819a'
      charset += u'\u8ce6\u8b5c\u4fae\u6b66\u90e8\u821e\u5c01\u98a8\u4f0f\u670d'
      charset += u'\u526f\u5e45\u5fa9\u798f\u8179\u8907\u8986\u62c2\u6cb8\u4f5b'
      charset += u'\u7269\u7c89\u7d1b\u96f0\u5674\u58b3\u61a4\u596e\u5206\u6587'
      charset += u'\u805e\u4e19\u5e73\u5175\u5002\u7add\u67c4\u965b\u9589\u5840'
      charset += u'\u5e63\u5f0a\u853d\u9920\u7c73\u58c1\u74a7\u7656\u5225\u8511'
      charset += u'\u7247\u908a\u8fd4\u8b8a\u504f\u904d\u7de8\u8faf\u4fbf\u52c9'
      charset += u'\u6b65\u4fdd\u54fa\u6355\u88dc\u8217\u6bcd\u52df\u5893\u6155'
      charset += u'\u66ae\u7c3f\u65b9\u5305\u82b3\u90a6\u5949\u5bf6\u62b1\u653e'
      charset += u'\u6cd5\u6ce1\u80de\u4ff8\u5023\u5cf0\u7832\u5d29\u8a2a\u5831'
      charset += u'\u8702\u8c50\u98fd\u8943\u7e2b\u4ea1\u4e4f\u5fd9\u574a\u59a8'
      charset += u'\u5fd8\u9632\u623f\u80aa\u67d0\u5192\u5256\u7d21\u671b\u508d'
      charset += u'\u5e3d\u68d2\u8cbf\u8c8c\u66b4\u81a8\u8b00\u9830\u5317\u6728'
      charset += u'\u6734\u7267\u7766\u50d5\u58a8\u64b2\u6ca1\u52c3\u5800\u672c'
      charset += u'\u5954\u98dc\u51e1\u76c6\u9ebb\u6469\u78e8\u9b54\u6bcf\u59b9'
      charset += u'\u679a\u6627\u57cb\u5e55\u819c\u6795\u53c8\u672b\u62b9\u842c'
      charset += u'\u6eff\u6162\u6f2b\u672a\u5473\u9b45\u5cac\u5bc6\u871c\u8108'
      charset += u'\u5999\u6c11\u7720\u77db\u52d9\u7121\u5922\u9727\u5a18\u540d'
      charset += u'\u547d\u660e\u8ff7\u51a5\u76df\u9298\u9cf4\u6ec5\u514d\u9762'
      charset += u'\u7dbf\u9eb5\u8302\u6a21\u6bdb\u5984\u76f2\u8017\u731b\u7db2'
      charset += u'\u76ee\u9ed8\u9580\u7d0b\u554f\u51b6\u591c\u91ce\u5f4c\u5384'
      charset += u'\u5f79\u7d04\u8b6f\u85e5\u8e8d\u95c7\u7531\u6cb9\u55a9\u6109'
      charset += u'\u8aed\u8f38\u7652\u552f\u53cb\u6709\u52c7\u5e7d\u60a0\u90f5'
      charset += u'\u6e67\u7336\u88d5\u904a\u96c4\u8a98\u6182\u878d\u512a\u8207'
      charset += u'\u8c6b\u9918\u8b7d\u9810\u5e7c\u7528\u7f8a\u5996\u6d0b\u8981'
      charset += u'\u5bb9\u5eb8\u63da\u6416\u8449\u967d\u6eb6\u8170\u6a23\u760d'
      charset += u'\u8e0a\u7aaf\u990a\u64c1\u8b20\u66dc\u6291\u6c83\u6d74\u6b32'
      charset += u'\u7fcc\u7ffc\u62c9\u88f8\u7f85\u4f86\u96f7\u8cf4\u7d61\u843d'
      charset += u'\u916a\u8fa3\u4e82\u5375\u89bd\u6feb\u85cd\u6b04\u540f\u5229'
      charset += u'\u91cc\u7406\u75e2\u88cf\u5c65\u7483\u96e2\u9678\u7acb\u5f8b'
      charset += u'\u6144\u7565\u67f3\u6d41\u7559\u9f8d\u7c92\u9686\u786b\u4fb6'
      charset += u'\u65c5\u865c\u616e\u4e86\u5169\u826f\u6599\u6dbc\u7375\u9675'
      charset += u'\u91cf\u50da\u9818\u5bee\u7642\u77ad\u7ce7\u529b\u7da0\u6797'
      charset += u'\u5398\u502b\u8f2a\u96a3\u81e8\u7460\u6dda\u7d2f\u58d8\u985e'
      charset += u'\u4ee4\u79ae\u51b7\u52f5\u623e\u4f8b\u9234\u96f6\u9748\u96b7'
      charset += u'\u9f61\u9e97\u66c6\u6b77\u5217\u52a3\u70c8\u88c2\u6200\u9023'
      charset += u'\u5ec9\u7df4\u934a\u5442\u7210\u8cc2\u8def\u9732\u8001\u52de'
      charset += u'\u5f04\u90de\u6717\u6d6a\u5eca\u6a13\u6f0f\u7c60\u516d\u9304'
      charset += u'\u9e93\u8ad6\u548c\u8a71\u8cc4\u8107\u60d1\u67a0\u7063\u8155'

  charset = "".join(set(charset)) # remove duplicates
  if charset == " ": # some joker tries to make a password of only spaces
    charset = ".-"

  # Convert bits to length or vice versa
  if mode == "bit":
    target_entropy = length
    target_length = int(ceil(target_entropy/(log(len(charset),2))))
  elif mode == "byte":
    target_entropy = length*8
    target_length = int(ceil((target_entropy)/(log(len(charset),2))))
  elif mode == "char":
    target_length = length
    target_entropy = None
  else:
    print "wait what"

  # generate password
  pw = ""
  for n in range(1,target_length+1):
    pw += random.SystemRandom().choice(charset)

  if verbose:
    actual_entropy = log(len(charset)**target_length,2)

    strength_rating = int(actual_entropy)/16
    if strength_rating > 16:
      strength_rating = 16

    strengths = [
"""EXTREMELY WEAK.
Can be broken in milliseconds.""", # 0
"""VERY WEAK.
Can be broken within hours on a standard PC.""", #16
"""WEAK.
A $5,000 PC setup can break this within a day.""", # 32
"""MODERATE.
A $5,000 PC setup can break this password within a year.""", # 48
"""QUITE STRONG.
Can be broken within a year by 2016's supercomputers, or high-end PCs by 2036.""", # 64
"""VERY STRONG.
Can be broken by a cutting edge exascale supercomputer within ten years.""", # 80
"""VERY STRONG.
Unbreakable even by the supercomputers of 2036.""", # 96
"""EXTREMELY STRONG.
Probably unbreakable even by supercomputers in 2056.""", # 112
"""UNBREAKABLE.
"128-bit classical computer brute force searches are impossible."
 -- Bruce Schneier""", # 128
"""UNBREAKABLE.
"128-bit classical computer brute force searches are impossible."
 -- Bruce Schneier""", # 144
"""UNBREAKABLE.
"128-bit classical computer brute force searches are impossible."
 -- Bruce Schneier""", # 160
"""UNBREAKABLE.
"128-bit classical computer brute force searches are impossible."
 -- Bruce Schneier""", # 176
"""MATHEMATICALLY UNBREAKABLE.
"If we built a Dyson sphere around the sun and captured all its energy for 32
years, without any loss, we could power a computer to counter up to 2^192."
 -- Bruce Schneier, Applied Cryptography""", # 192
"""COSMICALLY UNBREAKABLE.
"A typical supernova releases something like 10^51 ergs... If all of this
energy could be channeled into a single orgy of computation, a 219-bit counter
could be cycled through all of its states."
 -- Bruce Schneier, Applied Cryptography""", # 208
"""COSMICALLY UNBREAKABLE.
"A typical supernova releases something like 10^51 ergs... If all of this
energy could be channeled into a single orgy of computation, a 219-bit counter
could be cycled through all of its states."
 -- Bruce Schneier, Applied Cryptography""", # 224
"""COSMICALLY UNBREAKABLE.
"A typical supernova releases something like 10^51 ergs... If all of this
energy could be channeled into a single orgy of computation, a 219-bit counter
could be cycled through all of its states."
 -- Bruce Schneier, Applied Cryptography""", # 240
"""UNIVERSALLY, PHYSICALLY UNBREAKABLE.
"Brute force attacks against 256-bit keys will be infeasible until computers are
built from something other than matter and occupy something other than space."
 -- Bruce Schneier, Applied Cryptography""", # 256
    ]

    print fill("Generating a {} {}{} password from {} (character set size {}{}).".format(length,
      mode,
      " or greater" * (mode in ["bit", "byte"]),
      cat_charsets(charsets), len(charset),
      (", password length {}".format(target_length))*(mode in["bit", "byte"])
      ), 79)

    print u"Your password is: {}".format(pw)
    if not space_forbidden:
      print
      pw_chunks = []
      for n in range(0,len(pw), 4):
        pw_chunks.append(pw[n:n+4])
      for line in wrap(string.join(pw_chunks), 76):
        print "  " + line
      print

    print "Strength: {:.2f} bits; {}".format(actual_entropy, strengths[strength_rating])
    
  else: # not verbose
    print pw

if __name__ == "__main__":
  main()
