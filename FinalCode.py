import numpy as np
from scipy import stats
import time
import warnings
import string
import matplotlib.pyplot as plt
import collections
import csv
import pandas as pd
from StrengthChecker import get_strength_bool, get_strength_dict

warnings.filterwarnings("ignore")


start = time.time()


print("Reading in Data...")
# read in data from file to a list
# data_f = open("smallDataSet.txt", 'r', encoding='utf8')  # Small Test Data
# data_f = open("300kData.txt", 'r', encoding='utf8')  # Medium Test Data
data_f = open("rockyouUTF8.txt", 'r', encoding='utf8')  # Full Data

data = []
for line in data_f:
    data.append(line)
data_f.close()

stop0 = time.time()
print(f" - Read in File: {stop0 - start:.2f}")


# convert list to np array
print("Converting List to Numpy Array...")
data = np.array(data)

diff = time.time() - stop0
print(f" - Converted to NP: {diff:.2f}")


print("Stripping Unwanted Characters...")
# strip new lines and blank lines from data
data = np.char.strip(data, chars='\n')

stop1 = time.time()
print(f" - Stripping Runs: {stop1 - stop0:.2f}")


print("Finding the Length of all Passwords...")
# Use vectorize function of numpy to help find the length of each password
length_checker = np.vectorize(len)
  
# Find the length of each password
length_data = length_checker(data)

stop2 = time.time()
print(f" - Created Length Array: {stop2 - stop1:.2f}")

# Calculate stats
print("Calculating Length Stats...")
max_len = np.max(length_data)
min_len = np.min(length_data)
mean_len = np.mean(length_data)
mode_len = stats.mode(length_data, axis=None)

print(f"Max: {max_len}, Min: {min_len}, Mean: {mean_len}, Mode: {mode_len[0][0]}")

stop3 = time.time()
print(f" - Length Stats: {stop3 - stop2:.2f}")


print("Counting Character Occurences...")
# Count characters in every password
char_count = collections.Counter()
for p in data:
    char_count.update(p)
# find the frequency of letters in data

freqData = list(char_count.values())
valueKeys = list(char_count.keys())
total_values = 0
i=0
enumerate(valueKeys)
enumerate(freqData)

while i != len(valueKeys)-1:
    if valueKeys[i].isalpha():
        total_values += freqData[i]
    else:
        del freqData[i]
        del valueKeys[i]
        i = i - 1
    i = i + 1

valueKeys, freqData = zip(*sorted(zip(valueKeys, freqData)))

freqData = list(freqData)
valueKeys = list(valueKeys)

if valueKeys[0] == '\x03':
    del freqData[0]
    del valueKeys[0]

for q in range(0, 26):
    freqData[q] += freqData[q+26]
    freqData[q] = freqData[q] / total_values
    freqData[q]*=100
freqData = freqData[:26]

# print(char_count)

# Export dict as csv'
csv_columns = ['No', 'Char', 'Count']
with open("CharCount.csv", 'w') as f:
    writer = csv.writer(f)
    for key, value in char_count.items():
        try:
            writer.writerow([key, value])
        except:  # Needed to avoid errors when trying to write unwritable characters
            pass
f.close()

# Order dict in more appealing bar chart order and make it a percentage
total_chars = length_data.sum()
temp = {}
for c in string.printable:
    try:
        temp[c] = char_count[c] / total_chars
    except ValueError:
        pass
char_count = temp
del temp
# Create bar graph of all characters
names = list(char_count.keys())
values = list(char_count.values())
plt.figure(figsize=(15,5))
plt.title("Total Number of Every Character")
plt.bar(range(len(char_count)), values, tick_label=names)
# plt.show()
plt.savefig("CharCount.png")
plt.close()

stop4 = time.time()
print(f" - Counted Chars: {stop4 - stop3:.2f}")


print("Counting Number of Passwords with Punctuation...")
# Count number of passwrods containing special chars (punctuation)
special_char_count = 0
for line in data:
    for i in line:
        if i in string.punctuation:
            special_char_count += 1
            break
print(f"Number of passwords containing a special character: {special_char_count}")

stop5 = time.time()
print(f" - Num with Special: {stop5 - stop4:.2f}")

print("Analyzing Frequency of Letters...")


# Compares most common characters in english language to most common characters in dataset
freq_f = open("freq.txt", 'r', encoding='utf8')  
freqEng = []
for line in freq_f:
    freqEng.append(line)
freq_f.close()
freqEng = np.char.strip(freqEng, chars='\n')
freqEng.sort()
# frequency of english letters 

for i in range(0, len(freqEng)):
    freqEng[i] = freqEng[i][1:]
freqEng = list(np.float_(freqEng))

# adds lowercase and capital frequency in our data 

# creates letters for x label
letters = []
letters = list(string.ascii_uppercase)

# create plot 
X_axis = np.arange(len(letters))
plt.figure(figsize=(13,5))
plt.title("Freqency of Letters Between Password Data and English Words")

plt.bar( X_axis + .2, freqData, 0.4)
plt.bar( X_axis - .2, freqEng, 0.4  )
plt.legend(["Freqency in Passwords", "Frequency in English Words"])
plt.xlabel("Letters")
plt.ylabel("Freqency in Percent")
plt.xticks(X_axis, letters)
plt.savefig("LetterCount.png")
# plt.show()
plt.close()

print("Analyzing Password Strengths...")
# Check p-word strengths that pass all tests
strength_check_bool = np.vectorize(get_strength_bool)
strength_data_bool = strength_check_bool(data)

print(f"Number of Passwords that meet all Requirements: {strength_data_bool.sum()}")

# get p-word strength dicts
strength_check_dicts = np.vectorize(get_strength_dict)
strength_data_dicts = strength_check_dicts(data)

strength_data_dicts = pd.DataFrame(strength_data_dicts.tolist())
print(strength_data_dicts.head())

strength_results = {}
strength_results["MIN_LENGTH"] = strength_data_dicts["MIN_LENGTH"].sum()
strength_results["REQUIRE_LOWER"] = strength_data_dicts["REQUIRE_LOWER"].sum()
strength_results["REQUIRE_UPPER"] = strength_data_dicts["REQUIRE_UPPER"].sum()
strength_results["REQUIRE_NUM"] = strength_data_dicts["REQUIRE_NUM"].sum()
strength_results["REQUIRE_SPECIAL"] = strength_data_dicts["REQUIRE_SPECIAL"].sum()
print(f"Number of Passwrods that Pass Certain Tests: {strength_results}")

plt.figure(figsize=(10,5))
plt.bar(range(len(strength_results)), list(strength_results.values()), align='center')
plt.xticks(range(len(strength_results)), list(strength_results.keys()))
plt.title("Password Strength Metrics")
plt.savefig("PasswordStrengthMetrics.png")
# plt.show()


stop5 = time.time()
print(f" - Password Strengths: {stop5 - stop4:.2f}")


print(f"Total Time: {stop5 - start:.2f}")