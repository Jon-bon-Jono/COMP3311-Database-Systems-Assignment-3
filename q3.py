# Written by Jonathan Williams (z5162987), November 2019
# COMP3311 19T3 Assignment 3

import sys
import cs3311
conn = cs3311.connect()

cur = conn.cursor()

code_prefix = str(sys.argv[1]) if len(sys.argv) >=2 else "ENGG"

#for each meeting get the course code and building name
meeting_building_query = '''
select s.code, b.name
from meetings m 
inner join classes cl on (m.class_id = cl.id)
inner join courses cr on (cl.course_id = cr.id)
inner join subjects s on (s.id = cr.subject_id)
inner join rooms r on (r.id = m.room_id)
inner join buildings b on (b.id = r.within)
inner join terms t on (cr.term_id = t.id)
where s.code ilike '%'''+str(code_prefix)+'''%'
and t.name = '19T2'
group by b.name, s.code
order by b.name, s.code
'''
buildings_courses = {} #holds a list of courses for each building name
cur.execute(meeting_building_query)
for tup in cur.fetchall():
   course_code, building_name = tup
   #if building name not in dict, add it with an empty list
   if building_name not in buildings_courses.keys():
      buildings_courses[building_name] = []
   buildings_courses[building_name].append(course_code)
   
for building in sorted(buildings_courses.keys()):
   print(building)
   #for all courses in building, print course code
   for course in buildings_courses[building]:
      print(" "+str(course))
cur.close()
conn.close()
