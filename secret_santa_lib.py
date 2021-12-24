import random

import numpy as np


# A participant.
class Person:
  def __init__(self, name, email):
    self._name = name
    self._email = email

  def name(self):
    return self._name

  def email(self):
    return self._email


class Santa():

  def __init__(self, participants_path, do_not_match_path=None):
    # self._participants is a list of Person.
    self._participants = []
    with open(participants_path) as f:
      for line in f:
        person = line.strip().split(',')
        self._participants.append(Person(person[0], person[1]))
    self._num_participants = len(self._participants)
    self._name_to_id = {}
    for id, person in enumerate(self._participants):
      self._name_to_id[person.name()] = id
    
    # Matrix representation of matches, where self-matches and explicitly given
    # do-not-match sets are disallowed (i.e. set to False).
    self._template_matrix = np.invert(np.eye(self._num_participants, dtype=bool))
    if do_not_match_path:
      with open(do_not_match_path) as f:
        for line in f:
          group = line.strip().split(',')
          for name1 in group:
            id1 = self.get_id(name1)
            for name2 in group:
                id2 = self.get_id(name2)
                self._template_matrix[id1, id2] = False

  def get_person(self, id):
    return self._participants[id]

  def get_id(self, name):
    return self._name_to_id[name]

  def try_to_generate_match(self):
    matrix = np.copy(self._template_matrix)
    rng = np.random.default_rng()
    # Randomize row-processing order, or else bias accumulates.
    random_idxs = list(range(self._num_participants))
    random.shuffle(random_idxs)
    for row in random_idxs:
      arr = matrix[row, :]
      if sum(arr) == 0:
        return []  # Failed to generate assignment.
      picked_id = rng.choice(np.nonzero(arr)[0])
      matrix[row, :] = False
      matrix[:, picked_id] = False
      matrix[row, picked_id] = True

    assignment = {}
    for row in range(self._num_participants):
      matches = np.nonzero(matrix[row, :])[0]
      assert(len(matches) == 1)
      col = matches[0]
      assignment[row] = col
    return assignment

  # Draws matches until one succeeds.
  def match(self):
    while True:
      assignment = self.try_to_generate_match()
      if len(assignment) > 0:
        return assignment