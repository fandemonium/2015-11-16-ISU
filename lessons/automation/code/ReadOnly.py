#!/usr/bin/env python
 
import string
import sys
import os

DELIMITERS = [".", ",", ";", ":", "?", "$", "@", "^", "<", ">", "#", "%", "`", "!", "*", "-", "=", "(", ")", "[", "]", "{", "}", "/", "\"", "\'"]

"""

"""
def load_text(file):
  text = ""
  with open(file) as f:
    lines = f.read().splitlines()
  return lines

"""

"""
def save_word_counts(file, counts):
  f = open(file, 'w')
  for count in counts:
    f.write("%s\n" % " ".join(map(str, count)))
  f.close()

"""

"""
def load_word_counts(file):
  counts = []
  f = open(file, "r")
  for line in f:
    if (not line.startswith("#")):
      fields = line.split()
      counts.append((fields[0], int(fields[1]), float(fields[2])))
  f.close()
  return counts

"""

"""
def update_word_counts(line, counts):
  for purge in DELIMITERS:
    line = line.replace(purge, " ")
  words = line.split()
  for word in words:
    word = word.lower().strip()
    if word in counts:
      counts[word] += 1
    else:
      counts[word] = 1

"""

"""
def calculate_word_counts(lines):
  counts = {}
  for line in lines:
    update_word_counts(line, counts)
  return counts

"""

"""
def word_count_dict_to_tuples(counts, decrease = True):
  return sorted(iter(list(counts.items())), key=lambda key_value: key_value[1], \
    reverse = decrease)

"""

"""
def filter_word_counts(counts, min_length = 1):
  stripped = []
  for (word, count) in counts:
    if (len(word) >= min_length):
      stripped.append((word, count))
  return stripped

"""

"""
def calculate_percentages(counts):
  total = 0
  for count in counts:
    total += count[1]
  tuples = [(word, count, (float(count) / total) * 100.0) 
    for (word, count) in counts]
  return tuples

"""

"""
def word_count(input_file, output_file, min_length = 1):
  lines = load_text(input_file)
  counts = calculate_word_counts(lines)
  sorted_counts = word_count_dict_to_tuples(counts)
  sorted_counts = filter_word_counts(sorted_counts, min_length)
  percentage_counts = calculate_percentages(sorted_counts)
  save_word_counts(output_file, percentage_counts)

def check_against_unix(input_file, output_file, min_length=1):
	'''A function to check our file against unix wc'''
	command = "sort creatures/unicorn.dat | wc > unix_check"
	os.system(command)	

def make_output():
	if 'processed' in os.listdir('.'):
		print 'Processed directory exists'
	else:
		os.mkdir('processed')
		print 'Processed directory created'   

if  __name__ =='__main__':
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  min_length = 1
  if (len(sys.argv) > 3):
    min_length = int(sys.argv[3])
  make_output()  
  word_count(input_file, output_file, min_length)
  check_against_unix(input_file, output_file, min_length)