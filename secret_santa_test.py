import secret_santa_lib as santa

import numpy as np
import unittest

PARTICIPANTS = 'testdata/participants.txt'
EXCLUSIONS = 'testdata/do_not_match.txt'
INDEXES = {'a@a': 0,
           'b@b': 1,
           'c@c': 2,
           'd@d': 3,
           'e@e': 4}


def sanity_check(matches):
  hits = update_counts(np.zeros([5, 5]), matches)
  vert_sum = hits.sum(axis=0)
  horiz_sum = hits.sum(axis=1)
  ones = np.ones(len(INDEXES))
  np.testing.assert_array_equal(vert_sum, ones)
  np.testing.assert_array_equal(horiz_sum, ones)

def update_counts(counts, matches):
  for sender, recipient in matches.items():
    s_idx = INDEXES[sender]
    r_idx = INDEXES[recipient]
    counts[s_idx, r_idx] += 1
  return counts

class TestSecretSanta(unittest.TestCase):

  def setUp(self):
    self.participants = santa.parse_participants(PARTICIPANTS)

  def test_constraints(self):
    exclusions = santa.parse_bad_matches(EXCLUSIONS)
    matches = santa.match(self.participants, exclusions)
    #self.assertEqual(matches['a@a'], 'e@e')
    #self.assertEqual(matches['e@e'], 'a@a')

  def test_randomness(self):
    trials = int(1e5)
    counts = np.zeros([5, 5])
    print(f'Running {trials} trails...')
    for i in range(trials):
      if i % int(1e4) == 0:
        print(f'Ran {i} trials...')
      matches = santa.match(self.participants, {})
      sanity_check(matches)
      update_counts(counts, matches)
    probs = counts / trials
    for i in range(5):
      for j in range(5):
        if i == j:
          continue
        self.assertAlmostEqual(probs[i, j], 0.25, places=2)


if __name__ == '__main__':
    unittest.main()