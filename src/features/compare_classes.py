"""Are homophones more likely to be of the same grammatical category?"""

import pandas as pd
from tqdm import tqdm
import itertools
import editdistance as ed

import numpy as np

from config import PROCESSED_PATH


ITERATIONS = 100
df = pd.read_csv(PROCESSED_PATH)

print("Loading homophones")
df_homophones = pd.read_csv("data/processed/homophone_comparisons.csv")
homophones = list(df_homophones['w1']) + list(df_homophones['w2'])
print("Filtering on words that have a homophone pair...")
df = df[df['Word'].isin(homophones)]
print("#Words after: {num}\n".format(num=len(df)))

df['new_repr'] = df['PhonDISC'] + "**" + df['Class']

analysis = []

# Get true distribution
print("Getting combinations of all pairs...")

def compare_words(repr):
	combinations = list(itertools.combinations(repr, 2))

	for w1, w2 in combinations:
		# w1_row, w2_row = df[df['id']==w1], df[df['id']==w2]
		if type(w1) == float or type(w2) == float:
			continue
		phon1, class1 = w1.split("**")
		phon2, class2 = w2.split("**")

		same_class = class1 == class2

		difference = ed.eval(phon1, phon2)
		is_homophone = True if difference == 0 else False
		analysis.append({
			'same_class': same_class,
			'is_homophone': is_homophone
			})
	return pd.DataFrame(analysis)

def get_ratios(df_analysis):
	true_ratio_homophones = len(df_analysis[(df_analysis['is_homophone']==True) & (df_analysis['same_class']==True)]) / len(df_analysis[(df_analysis['is_homophone']==True) & (df_analysis['same_class']==False)])
	true_ratio_non = len(df_analysis[(df_analysis['is_homophone']==False) & (df_analysis['same_class']==True)]) / len(df_analysis[(df_analysis['is_homophone']==False) & (df_analysis['same_class']==False)])
	return true_ratio_homophones, true_ratio_non

df_analysis = compare_words(df['new_repr'])
true_ratios = get_ratios(df_analysis)

homophone_shuffle_ratios, non_homophone_shuffle = [], []
classes = list(df['Class'])
for iteration in range(ITERATIONS):
	print(iteration)
	permuted = np.random.permutation(classes)
	new_repr = df['PhonDISC'] + "**" + permuted
	df_analysis_copy = compare_words(new_repr)
	new_ratios = get_ratios(df_analysis_copy)
	homophone_shuffle_ratios.append(new_ratios[0])
	non_homophone_shuffle.append(new_ratios[1])

