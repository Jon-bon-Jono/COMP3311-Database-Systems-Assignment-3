# Written by Jonathan Williams (z5162987), November 2019
# COMP3311 19T3 Assignment 3

import sys
import cs3311
conn = cs3311.connect()

cur = conn.cursor()

course_code = str(sys.argv[1]) if len(sys.argv) >=2 else "COMP1521"
#query to get info on class_id, class type, class quota and number of class enrolments
class_query = '''
select cl.id, ct.name, cl.tag, cl.quota, count(*)
from class_enrolments ce
inner join classes cl on (cl.id = ce.class_id)
inner join classtypes ct on (cl.type_id = ct.id)
inner join courses cr on (cr.id = cl.course_id)
inner join subjects s on (cr.subject_id = s.id)
inner join terms t on (t.id = cr.term_id)
where s.code = %s and t.name = '19T3'
group by cl.id, ct.name, cl.tag, cl.quota
order by ct.name, cl.tag
'''

cur.execute(class_query, [course_code])
for tup in cur.fetchall():
   class_id, class_type, class_tag, quota, num_enroled = tup
   percentage_full = round(int(num_enroled)/int(quota)*100)
   #only prints classes that are less than half full
   if(int(num_enroled)/int(quota) < 0.5):
      print(class_type+" "+class_tag.strip()+" is "+str(percentage_full)+"% full")


cur.close()
conn.close()
