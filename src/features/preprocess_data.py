"""
Empirical question: Are the meanings of homophones more dissociable by context than you’d expect by chance?

Questions to ask:

1. Identify all homophones using CELEX data. Then, ask: do homophones usually span grammatical class? 
2. Identify heterographic homophones using CELEX. Then, ask: do they have more different meanings than by chance?

For both (1) and (2), homophones just have 0 edit distances.

Things to make sure of:
Things to make sure of:
1. Make sure they are homophones in the dialect of the language we’re doing the corpus analysis on.
2. Make sure that they’re actually homophones, not just alternate spellings. 
3. Make sure the homophones / homonyms aren’t less frequent overall than the other words. 

For (3), include in the ultimate regression multiple covariates, including:
1. Frequency
2. Length of word
3. Same / different grammatical class
Since regression is predicting word *pairs*, can solve (1) and (2) using a column for:
- "more frequent word word frequency"
- "less frequent word word frequency"
(And same for length.)

Could also ask --> are homophones more or less systematic than non-homophones? (Do leave-one-out, and
regress arbitrariness ~ homophones). 
Asks a slightly different question: not "are homophone pairs more dissimilar than the average word-pair?",
but rather --> "do homophones have formal properties that attract similar kinds of meanings?"

"""

import pandas as pd


from config import HOMOPHONE_PATH, CELEX_PATH, REMOVE_PATH, MULTIPLE_SPELLINGS, PROCESSED_PATH, REMOVE_ALL_HOMONYMS

# Load CELEX words
df = pd.read_csv(CELEX_PATH, sep="\\")
df['id'] = range(len(df))

# Remove words that aren't all lowercase
print("Removing words that are not all lowercase.")
df = df[df['Word'].str.islower().fillna(False)]
print("#Words after: {num}\n".format(num=len(df)))

# Select only monomorphemic, monosyllabic words
print("Selecting only monomorphemic, monosyllabic words")
print("#Words before: {num}".format(num=len(df)))
df = df[df['CompCnt'] <= 1]
df = df[df['SylCnt'] <= 1]
print("#Words after: {num}\n".format(num=len(df)))

# Remove words from "remove" list
print("Removing words from specified list.")
with open(REMOVE_PATH, "r") as input_file:
	to_remove = input_file.read().split("\n")

df = df[~df['Word'].isin(to_remove)]
print("#Words after: {num}\n".format(num=len(df)))

# Deal with words with multiple spellings
print("Removing words with multiple spellings")
multiple_spellings = pd.read_csv(MULTIPLE_SPELLINGS)
df = df[~df['Word'].isin(multiple_spellings['w1'])]
df = df[~df['Word'].isin(multiple_spellings['w2'])]
print("#Words after: {num}\n".format(num=len(df)))

# Remove homonyms that span multiple classes
# (Alternatively, choose the homonym with the highest frequency)
if REMOVE_ALL_HOMONYMS:
	print("Removing all words that have one or more homonyms.")
	words_with_homonyms = df[df.duplicated(subset="Word")]['Word']
	print("Number of words with multiple entries: {num}".format(num=len(words_with_homonyms)))
	df = df[~df['Word'].isin(words_with_homonyms)]
else:
	print("Preserving the highest-frequency words of each homonym set.")
	df = df.sort_values('CobLog', ascending=False).drop_duplicates('Word').sort_index()
print("Number of words left: {num}\n".format(num=len(df)))

# Save to .csv file
print("Saving to .csv file: {path}".format(path=PROCESSED_PATH))
df.to_csv(PROCESSED_PATH)




