# Written by Jonathan Williams (z5162987), November 2019
# COMP3311 19T3 Assignment 3

import sys
import cs3311
conn = cs3311.connect()

cur = conn.cursor()

num_cases = int(sys.argv[1]) if len(sys.argv) >=2 else 2

course_digits = {} #dictionary for course_code digits
#get all subject codes
subject_query = '''
select s.code
from subjects s
'''
#populate the dictionary with course code digits
cur.execute(subject_query)
tup_list = cur.fetchall()
for tup in tup_list: 
   code =  ''.join(tup) 
   code = code[4:]
   course_digits[code] = course_digits.get(code, 0) + 1

sorted_keys = sorted(course_digits.keys())
for k in sorted_keys:
   if course_digits[k] == num_cases:
      #get all course codes that match the digits in k
      code_prefix_query = '''
      select s.code 
      from subjects s
      where s.code ilike '%'''+str(k)+'''%'
      order by s.code
      '''
      cur.execute(code_prefix_query)
      code_prefix_list = cur.fetchall()
      code_prefixs = ""
      #get only the text for each course code
      for tup in code_prefix_list:
         prefix =  ''.join(tup) 
         prefix = prefix[:4]
         code_prefixs = code_prefixs+" "+prefix
      print(k+":"+code_prefixs)

cur.close()
conn.close()
