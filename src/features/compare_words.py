"""Run after preprocessing CELEX data."""

import itertools

import editdistance as ed
import pandas as pd
from gensim.models import KeyedVectors

from tqdm import tqdm

from config import MODEL_PATH, PROCESSED_PATH

from nlp_utilities.compling import CorpusUtilities

# Load model
print("Loading model...")
model = KeyedVectors.load_word2vec_format(MODEL_PATH, binary=True) 

# Load processed data
df = pd.read_csv(PROCESSED_PATH)

# Keep only words from word2vec model
print("Filtering out words not in word2vec model...")
df_subset = df[df['Word'].isin(model.vocab)]
print("{words} words from word2vec model.".format(words=len(df_subset)))

## Analysis
analysis = []
print("Generating combinations")
combinations = list(itertools.combinations(df_subset['id'], 2))
print("Combinations: {combinations}".format(combinations=len(combinations)))
for w1, w2 in tqdm(combinations):
	w1_row, w2_row = df_subset[df_subset['id']==w1], df_subset[df_subset['id']==w2]
	# Orthographic distance
	w1_word, w2_word = w1_row['Word'].iloc[0], w2_row['Word'].iloc[0]
	orthographic_distance = ed.eval(w1_word, w2_word)
	# Are the words the same class?
	same_class = w1_row['Class'].iloc[0] == w2_row['Class'].iloc[0]
	# Get phonetic distance
	phon1, phon2 = w1_row['PhonDISC'].iloc[0], w2_row['PhonDISC'].iloc[0]
	phonetic_distance = ed.eval(phon1, phon2)
	# are they homophones? if so, heterographic?
	is_homophone = phon1 == phon2
	is_homonym = w1_word == w2_word
	# Get respective orthographic neighborhood sizes
	orthographic_neighborhood_w1 = CorpusUtilities.orthographic_similarity(
		word=w1_word, lexicon=list(df_subset['Word']))
	orthographic_neighborhood_w2 = CorpusUtilities.orthographic_similarity(
		word=w2_word, lexicon=list(df_subset['Word']))
	# get meaning distance
	meaning_distance = model.similarity(w1_word, w2_word)
	# Get frequencies
	high_freq = max([w1_row['CobLog'].iloc[0], w2_row['CobLog'].iloc[0]])
	low_freq = min([w1_row['CobLog'].iloc[0], w2_row['CobLog'].iloc[0]])
	# get lengths
	long_length = max([len(phon1), len(phon2)])
	short_length = min([len(phon1), len(phon2)])
	# Append to list
	analysis.append({
		'high_freq': high_freq,
		'low_freq': low_freq,
		'w1': w1_word,
		'w2': w2_word,
		'phon1': phon1,
		'phon2': phon2,
		'phonetic_distance': phonetic_distance,
		'orthographic_distance': orthographic_distance,
		'long_length': long_length,
		'short_length': short_length,
		'meaning_distance': meaning_distance,
		'orthographic_neighborhood_w1': orthographic_neighborhood_w1,
		'orthographic_neighborhood_w2': orthographic_neighborhood_w2,
		'same_class': same_class,
		'is_homophone': is_homophone,
		'is_homonym': is_homonym
		})

	
df_analysis = pd.DataFrame(analysis)
df_analysis.to_csv("data/processed/wordpair_comparisons.csv")