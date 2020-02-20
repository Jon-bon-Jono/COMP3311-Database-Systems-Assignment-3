# Written by Jonathan Williams (z5162987), November 2019
# COMP3311 19T3 Assignment 3

import sys
import cs3311
conn = cs3311.connect()

cur = conn.cursor()

code_prefix = str(sys.argv[1]) if len(sys.argv) >=2 else "ENGG"
#query returns term name, course code and num students enrolled for that term
term_subj_count_query = '''
select t.name, s.code, count(*)
from course_enrolments ce
inner join courses c on (ce.course_id = c.id)
inner join terms t on (c.term_id = t.id)
inner join subjects s on (s.id = c.subject_id)
where s.code ilike '%'''+str(code_prefix)+'''%'
group by t.name, s.code
order by t.name, s.code
'''
cur.execute(term_subj_count_query)
tuples = cur.fetchall()
#curr_term used to trigger the printing of a term name
curr_term,_,_ = tuples[0]
print(curr_term)
for tup in tuples:
   term, course_code, num_enrolled = tup
   #tuples ordered by term name
   #if term has changed print new term name
   if(curr_term != term):
      curr_term = term
      print(curr_term)
   print(" "+course_code+"("+str(num_enrolled)+")")

cur.close()
conn.close()
