"""Config file."""

import os

# Set paths
HOMOPHONE_PATH = "data/raw/htest.csv"
CELEX_PATH = "data/raw/celex_all.csv"
REMOVE_PATH = "data/hand_annotated/remove.txt"
MULTIPLE_SPELLINGS = "data/hand_annotated/multiple_spellings.csv"
MODEL_PATH = os.environ['WORD2VEC_PATH']
PROCESSED_PATH = "data/processed/celex_processed.csv"

# Parameters
REMOVE_ALL_HOMONYMS = False