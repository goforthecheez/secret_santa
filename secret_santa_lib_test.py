import secret_santa_lib

import numpy as np
import unittest

PARTICIPANTS_PATH = 'testdata/participants.txt'
DO_NOT_MATCH_PATH = 'testdata/do_not_match.txt'


class TestSecretSanta(unittest.TestCase):

  def test_constraints(self):
    print('Run test_constraints:')
    santa = secret_santa_lib.Santa(PARTICIPANTS_PATH, DO_NOT_MATCH_PATH)
    matches = santa.match()
    a_x = santa.get_id("A X")
    a_y = santa.get_id("A Y")
    b = santa.get_id("B")
    c = santa.get_id("C")
    d = santa.get_id("D")
    f = santa.get_id("F")

    # There is only 1 valid match.
    self.assertTrue((a_x, a_y) in matches.items())
    self.assertTrue((a_y, a_x) in matches.items())
    self.assertTrue((b, d) in matches.items())
    self.assertTrue((c, f) in matches.items())
    self.assertTrue((d, b) in matches.items())
    self.assertTrue((f, c) in matches.items())
    print('PASS')

  def test_randomness(self):
    print('Run test_randomness:')
    trials = int(1e5)
    counts = np.zeros([6, 6])
    santa = secret_santa_lib.Santa(PARTICIPANTS_PATH)
    print(f'Running {trials} trials...')
    for i in range(trials):
      if i % int(1e4) == 0:
        print(f'Ran {i} trials...')
      matches = santa.match()
      for sender_id, recipient_id in matches.items():
        counts[sender_id, recipient_id] += 1
    probs = counts / trials
    print(probs)

    for i in range(5):
      for j in range(5):
        if i == j:
          continue
        self.assertAlmostEqual(probs[i, j], 0.2, places=2)
    print('PASS')


if __name__ == '__main__':
    unittest.main()