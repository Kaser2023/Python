
import csv



# For Digits
from string import digits

# For Letters
from string import ascii_letters

# For Symbols!!!
from string import punctuation

#  For all of them in one line:
# from string import digits, ascii_letters, punctuation

from itertools import product



# For ALL of them
for passcode in product(punctuation + digits + ascii_letters, repeat=8):
        print(*passcode)


# For Letters
for passcode in product(punctuation, repeat=4):
        print(*passcode)

# For Digits
# for passcode in product(digits, repeat=10):

# For Letters
# for passcode in product(ascii_letters, repeat=4):
#         print(*passcode)









'''
class Solution:
    def romanToInt(self, s: str) -> int:
        roman_to_integer = {'I': 1,
                                'V': 5,
                                'X': 10,
                                'L': 50,
                                'C': 100,
                                'D': 500,
                                'M': 1000}

        s = s.replace('IV', 'IIII') \
                .replace('IX', 'VIII') \
                .replace('XL', 'XXXX') \
                .replace('XC', 'LXXXX') \
                .replace('CD', 'CCCC') \
                .replace('CM', 'DCCCC')

        return sum(map(roman_to_integer.get, s))


    romanToInt("IV", 60)


'''























'''
from cs50 import SQL


db = SQL("sqlite:///newdatabase.db")

title = input("First Name: ").strip()

rows = db.execute("SELECT lastname  FROM kaser WHERE lastname LIKE ?", title)
# rows = db.execute("SELECT COUNT(*) AS counter FROM kaser WHERE firstname LIKE ?", title)
# the (?) after LIKE is same like (%s) in C.

counter = 0
for row in rows:
    print(row["lastname"])
    counter += 1

print(counter)

# row = rows[0]
# print(row["counter"])



'''












# with open("names.csv", "r") as file:
#
#     counter = 0
#
#     reader = csv.DictReader(file)
#     for row in reader:
#         title = row["Last Name"].strip().upper()
#         if title == ("Brown").upper() or title == ("brown").upper():
#             counter += 1
#
#
# print(f"The number of people who has [Allen] name: {counter} ")
#



















# import csv
#
# with open("names.csv", "r") as file:
#
#     titels = {}
#     reader = csv.DictReader(file)
#     for row in reader:
#         title = row["First Name"].strip().upper()
#         if not title in titels:
#             titels[title] = 0
#         titels[title] += 1
#
# def get_value(title):
#     return titels[title]
#
# #this will sort the output!!!
# for title in sorted(titels, key=lambda title: titels[title], reverse=True):
# # for title in sorted(titels, key=get_value, reverse=True):
#     print(title, titels[title])
#         print(title)

# for title in titels:
#     print(title, titels[title])








# with open("cs50.csv", "r") as file:
# with open("movies.csv", "r") as file:
# with open("names.csv", "r") as file:
#
#     titels = []
#
#     reader = csv.DictReader(file)
#     for row in reader:
#         title = row["First Name"].strip().upper()
#         if not title in titels:
#             titels.append(title)
#
#         # if not row["First Name"] in titels:
#         #     titels.append(row["First Name"])
#
#
#
#
# for title in titels:
#         print(title)
#










#
# with open("movies.csv", "r") as file:
#
#     # reader = csv.reader(file)
#     # the next(reader) will ignore the first line of the <.csv> file
#     # next(reader)
#
#     # here we read the csv file depending on Dictionary
#     reader = csv.DictReader(file)
#     for row in reader:
#         print(row["Genre"])




