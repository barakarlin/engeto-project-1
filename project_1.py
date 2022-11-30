"""
projekt_1.py: první projekt do Engeto Online Python Akademie
author: Bara Karlinova
email: bara.karlinova@kiwi.com
discord: BaraKar#6094
"""

import pandas as pd
import re

from io import StringIO

from task_template import TEXTS

separator = "-" * 40

# Vyžádá si od uživatele přihlašovací jméno a heslo
user = input("Username: ")
password = input("Password: ")

# Zjistí, jestli zadané údaje odpovídají někomu z registrovaných uživatelů
# Pokud je registrovaný, pozdrav jej a umožni mu analyzovat texty
# Pokud není registrovaný, upozorni jej a ukonči program

# users = ['bob', 'ann', 'mike', 'liz']
# passwords = [123, 'pass123', 'password123', 'pass123']
# passwords = [str(x) for x in passwords]

registered_users = """
+------+-------------+
| user |   password  |
+------+-------------+
| bob  |     123     |
| ann  |   pass123   |
| mike | password123 |
| liz  |   pass123   |
+------+-------------+
"""

# remove + and - characters from string
registered_users = re.sub(r"[+-]", "", registered_users)
# convert to pandas data frame
registered_users = pd.read_csv(StringIO(registered_users), sep="|")
# remove whitespaces from column names
registered_users.columns = registered_users.columns.str.strip()
# select only desired columns
registered_users = registered_users.loc[:, ['user', 'password']]
# remove whitespaces from user
registered_users.loc[:, 'user'] = registered_users.loc[:, 'user'].str.strip()
# remove whitespaces from password
registered_users.loc[:, 'password'] = registered_users.loc[:, 'password'].str.strip()

# create separate lists containing usernames and passwords
users = registered_users.loc[:, 'user'].to_list()
passwords = registered_users.loc[:, 'password'].to_list()

# Pokud je uzivatel registrovany, pozdrav jej a umozni mu analyzovat texty
# Pokud neni registrovany, upozorni jej a ukonci program.
if user in users:  # if user is registered
    # check if password corresponds to the user
    if password in passwords and users.index(user) == passwords.index(password):
        print(separator,
              f"Welcome to the app, {user}",
              f"We have {len(TEXTS)} texts to be analyzed.",
              separator,
              sep='\n')
    else:
        print('Incorrect password, terminating the program.')
        exit()
else:
    print('Unregistered user, terminating the program.')
    exit()

# Program nechá uživatele vybrat mezi třemi texty, uloženými v proměnné TEXTS
text_num = input("Enter a number btw. 1 and 3 to select: ")

# Pokud uživatel vybere takové číslo textu, které není v zadání, program jej upozorní a skončí,
# Pokud uživatel zadá jiný vstup než číslo, program jej rovněž upozorní a skončí.
if not text_num.isnumeric():
    print('Non-numeric input, terminating the program.')
    exit()
elif not int(text_num) in range(1, len(TEXTS)+1):
    print('Input is out of range, terminating the program.')
    exit()

print(separator)

# Pro vybraný text spočítá následující statistiky:
# počet slov,
# počet slov začínajících velkým písmenem,
# počet slov psaných velkými písmeny,
# počet slov psaných malými písmeny,
# počet čísel (ne cifer),
# sumu všech čísel (ne cifer) v textu.

# create a list of words adjusted for punctuation
words_clean = list()
words = TEXTS[int(text_num)-1].split()

for word in words:
    words_clean.append(word.strip(",.:;?!"))

# compute statistics
# 30N would be counted twice in titlecase and uppercase words -> assigning it to titlecase words by limiting uppercase words
# only to letters; this way the statistics match those on Engeto
title_case_words = [x for x in words_clean if x.istitle()]
uppercase_words = [x for x in words_clean if x.isupper() and x.isalpha()]
# buff-to-white would not be counted if limiting only to letters, but it seems unnecessary to do so
lowercase_words = [x for x in words_clean if x.islower()]
numeric_strings = [x for x in words_clean if x.isnumeric()]
sum_numeric = sum([int(x) for x in numeric_strings])

print(f"There are {len(words)} words in the selected text.",
      f"There are {len(title_case_words)} titlecase words.",
      f"There are {len(uppercase_words)} uppercase words.",
      f"There are {len(lowercase_words)} lowercase words.",
      f"There are {len(numeric_strings)} numeric strings.",
      f"The sum of all the numbers is {sum_numeric}.",
      separator,
      sep="\n")

# Program zobrazí jednoduchý sloupcový graf, který bude reprezentovat četnost různých délek slov v textu.
words_hist = dict()

for word in words_clean:
    if len(word) not in words_hist:
        words_hist[len(word)] = 1
    else:
        words_hist[len(word)] = words_hist[len(word)] + 1

max_occurence = max(words_hist.values())

print(f'{"LEN|":>4}',
      f'{"OCCURENCES":^{max_occurence + 2}}',
      f'{"|NR.":<{len(separator) - max_occurence - 2}}')

print(separator)

for item in sorted(words_hist):
    print(f'{item:>3}|',
          f'{"*" * words_hist[item]:<{max_occurence + 2}}',
          f'|{words_hist[item]:<{len(separator) - max_occurence - 2}}')
    