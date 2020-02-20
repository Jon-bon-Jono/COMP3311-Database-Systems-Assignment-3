#Written by Jonathan Williams (z5162987) November 2019
# COMP3311 19T3 Assignment 3

import cs3311
conn = cs3311.connect()

cur = conn.cursor()
#query to fetch a courses quota and num_enrolled in 19T3 for courses with a quota more than 50
query = '''
select s.code, t.name, c.quota, n.num_enrolled 
from courses c 
inner join terms t on (c.term_id = t.id) 
inner join subjects s on (c.subject_id = s.id) 
inner join 
   (select c.id, count(e) as num_enrolled
    from courses c 
    inner join course_enrolments e on (c.id = e.course_id) 
    group by c.id
   ) n on (n.id = c.id) 
where t.name = '19T3' AND c.quota > 50
order by s.code
'''
cur.execute(query)
tup_list = cur.fetchall()
#print over enrolled courses
for tup in tup_list:
   code, term, quota, num_enrolled = tup
   if num_enrolled <= quota:
      continue
   print(str(code)+" "+str(round((num_enrolled/quota)*100))+"%")
cur.close()
conn.close()
