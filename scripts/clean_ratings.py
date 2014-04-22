"""
This file loads, merges, and cleans the ratings data from Wikipedia.
"""
import numpy as np
import pandas as pd

url = 'https://ckannet-storage.commondatastorage.googleapis.com/2012-10-22T184507/aft4.tsv.gz'

df = pd.read_csv('data/aft4.tsv.gz', compression='gzip', sep='\t')
df.info

# Egad, almost 50 million rows! Let's cut it down.
# We'll take a random sample of page_ids, then get all the ratings for those
# pages.

page_ids = pd.unique(df.page_id) # unique page_ids
sample_pids = np.random.choice(page_ids, 1000, replace=False) # sample of 1000

# Now cut the dataset to data for those 1000 pages
sample = df[df.page_id.isin(sample_pids)];
sample.info

# Much better!

# TODO
"""
keep only when namespace == 0
keep only when at least one rating on at least two different revisions
  make sure to sort by pid , rid, and timestamp

reshape wide with rating key/value, probably before doing other things
  --> this will mean that we can just look at the N to check if we have multiple ratings
  
we'll have to aggregate the revisions between ratings
  so if there are 3 edits between revisions, we'll need to figure out what the diff really is from one to the next
  