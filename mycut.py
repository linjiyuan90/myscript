#!/usr/bin/python3

'''
  cut command seems can't deal with situation where delimiters are also inside
  the field, such as: abc,"def,ghi",jk (the comma inside the double quote
  should not be split)
  
  This simple script simply fix this bug by combining neighbor fields.
'''

USAGE = \
'''Usage: python3 mycut.py file delimiters fields
fields looks like: 1-3,4-5,7, and it start from 1'''

import sys, os

def parse_fields(fields):
  lst = []
  for field in fields.split(','):
    x = field.split('-') 
    if len(x) == 2:
      x, y = int(x[0]), int(x[1])
      assert 0 < x <= y 
      lst.extend(range(x, y+1))
    else:
      assert len(x) == 1, 'fields format error: ' + field
      lst.append(int(x[0]))

  return sorted(lst)

def cut_fields(fields, delimiters, lines):
  out_lines = []
  num_fields = None  # set it as first line's num of fields
  for (ix, line) in enumerate(lines):
    line = line.strip()
    if not line:  # ignore empty line
      continue
    line = line.split(delimiters)
    # chars in string should not be treat as delimiters
    # for example: 1,'2,3',3
    # so, combine them
    p = 0
    while p < len(line):
      # note p may be empty
      if line[p] and (line[p][0] == '"' or line[p][0] == '\''):
        ch = line[p][0]
        while line[p][-1] != ch:
          line = line[:p] + [line[p] + line[p+1]] + line[p+2:]
      p += 1

    if not num_fields:
      num_fields = len(line)

    assert len(line) == num_fields, \
           "%dth line's num of fileds != 1st line's" % (ix+1)
    
    out_lines.append([line[j-1] for j in fields if j <= num_fields])
  
  return out_lines
 

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print(USAGE)
    exit(1)
  
  input = sys.argv[1]
  delimiters = sys.argv[2]
  fields = parse_fields(sys.argv[3])
  out_lines = cut_fields(fields, delimiters, open(input).readlines())
 
  for out_line in out_lines:
    print(delimiters[0].join(out_line))

