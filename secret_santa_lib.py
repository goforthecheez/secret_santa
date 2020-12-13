import copy
import random

# Returns map from email address to name.
def parse_participants(path):
  participants = {}
  with open(path) as f:
    for line in f:
      person = line.strip().split(',')
      participants[person[1]] = person[0]
  return participants

# Returns map from each email address with constraints to all email addresses
# it should not match to.
def parse_bad_matches(path):
  do_not_match = {}
  with open(path) as f:
    for line in f:
      people = line.strip().split(',')
      for x in people:
        do_not_match[x] = set(people) - set(x)
  return do_not_match

def is_self_match(a, b):
  return a == b

def is_bad_match(a, b, do_not_match):
  if a not in do_not_match:
    return False
  return b in do_not_match[a]

def has_bad_match(matches, do_not_match):
  for a, b in matches.items():
    if is_self_match(a, b) or is_bad_match(a, b, do_not_match):
      return True
  return False

# Draws matches until constraints are satisfied.
def match(participants, do_not_match):
  matches = {}
  while True:
    r_scratch = list(participants.keys())
    for sender in participants.keys():
      random.shuffle(r_scratch)
      recipient = r_scratch.pop()
      matches[sender] = recipient
    if not has_bad_match(matches, do_not_match):
      break
  return matches