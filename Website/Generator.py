import random

SmallChars = "abcdefghijklmnopqrstuvwxyz"
BigChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Nums = "0123456789"
SpecialChars = "#%&$@"

Chars = []
Password = ""
FivthPasswords = list()
for Param in Parameters:
    if Param == "UseNum":
        Chars += Nums
    if Param == "UseLettersSmall":
        Chars += SmallChars
    if Param == "UseLettersBig":
        Chars += BigChars
    if Param == "UseSpecialLetters":
        Chars += SpecialChars

for n in range(5):
    password =''
    for i in range(int(PasswordLength)):
        password += random.choice(Chars)
    print(password)