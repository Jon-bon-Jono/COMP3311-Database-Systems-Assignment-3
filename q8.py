# Written by Jonathan Williams (z5162987), November 2019
# COMP3311 19T3 Assignment 3

import sys
import cs3311
from datetime import datetime
from datetime import timedelta

#class for final timetable
#stores meetings in a dictionary
#adds class to timetable if it fits in timetable
class TimeTable: 
   #meetings: course_code, class name, stime, etime
   def __init__(self):
      self.meetings = {'Mon':[],'Tue':[],'Wed':[],'Thu':[],'Fri':[]}
      self.total_hours = 0
   
   #adds class_hours to the timetable's total_hours
   #adds class meetings to timetables meetings and returns true
   #returns false if any meetings clash with existing timetable meetings  
   def addClass(self,course_code, class_meetings):
      new_timetable_meetings = [] #list of tuples formated for the class
      class_hours = timedelta() #count hours for this class
      #check if this class fits in the timetable
      for new_meeting in class_meetings:
         nclass_name, new_day, nstime, netime = new_meeting
         #check for clashes with any classes already on that day
         for timetable_meeting in self.meetings[new_day]:
            t_code, t_clname, tday, tstime, tetime = timetable_meeting
            #if there is a clash, return false
            if (tstime < nstime < netime) or (tstime < netime < tetime):
               return False
         #count hours and format meeting tuples as we go
         new_timetable_meetings.append((course_code,nclass_name,new_day,nstime,netime))
         class_hours += (datetime.strptime(str(netime), '%H%M') - datetime.strptime(str(nstime), '%H%M'))
      #the class fits in the timetable, so we add each meeting for each day
      for new_meeting in new_timetable_meetings:
         _, _, new_day, _, _ = new_meeting
         self.meetings[new_day].append(new_meeting)
      self.total_hours += class_hours.total_seconds()/3600
      return True


conn = cs3311.connect()

cur = conn.cursor()

#using one query to get all meetings for the course/s this semester
query='''
select s.code, ct.tag, ct.name, cl.id, t.name, m.day, m.start_time, m.end_time
from meetings m
inner join classes cl on (cl.id = m.class_id) 
inner join courses cr on (cr.id = cl.course_id) 
inner join subjects s on (s.id = cr.subject_id)
inner join terms t on (cr.term_id = t.id)
inner join classtypes ct on (cl.type_id = ct.id)
inner join rooms r on (r.id = m.room_id)
where t.name = %s and r.code ilike %s and ('''
query_args = ["19T3", "K-%"]
required_classes = {} #nested dictionary to hold all meetings organised by class options

#if no args given, query for default courses
if len(sys.argv) < 2:
   query+= "s.code = 'COMP1511' or s.code='MATH1131')"
else:
   #else, for each given course arg, concatenate query and append to query_args 
   query += "s.code = %s"
   query_args.append(str(sys.argv[1]))
   for course in sys.argv[1:]:
      query += " or s.code = %s"
      query_args.append(str(course))
   query += ")"
   
cur.execute(query, query_args)
for tup in cur.fetchall():
   course_code, class_type, class_name, class_id, term, day, stime, etime = tup
   #using a nested dictionary for each of the options for a class
   #nested dictionary stores a list of meetings (tuple) for each class
   #required class is identified by course_code+class_type
   required_class = str(course_code)+" "+str(class_type)
   if required_class not in required_classes:
      required_classes[required_class] = {}
   if str(class_id) not in required_classes[required_class]:
      required_classes[required_class][str(class_id)] = []
   required_classes[required_class][str(class_id)].append((class_name,day,stime,etime))


#for reqclass in required_classes.keys():
#   print(reqclass)
#   for options in required_classes[reqclass].keys():
#      print(" ", required_classes[reqclass][options])


#construct valid timetable
timetable = TimeTable()
  #for each required_class, keep adding options until valid
for reqclass in required_classes.keys():
   #just choose first option (list of meetings) that makes the timetable valid
   for option in required_classes[reqclass]:
      course_code, class_type = reqclass.split()
      valid = timetable.addClass(course_code,required_classes[reqclass][option])
      if valid == True:
         break
#print timetable
print("Total hours: "+str(timetable.total_hours))
print("Mon") if timetable.meetings['Mon'] else None
for meeting in timetable.meetings['Mon']:
   course_code, class_name, _, stime, etime = meeting
   print("  "+course_code+" "+class_name+": "+str(stime)+"-"+str(etime))
print("Tue") if timetable.meetings['Tue'] else None
for meeting in timetable.meetings['Tue']:
   course_code, class_name, _, stime, etime = meeting
   print("  "+course_code+" "+class_name+": "+str(stime)+"-"+str(etime))
print("Wed") if timetable.meetings['Wed'] else None
for meeting in timetable.meetings['Wed']:
   course_code, class_name, _, stime, etime = meeting
   print("  "+course_code+" "+class_name+": "+str(stime)+"-"+str(etime))
print("Thu") if timetable.meetings['Thu'] else None
for meeting in timetable.meetings['Thu']:
   course_code, class_name, _, stime, etime = meeting
   print("  "+course_code+" "+class_name+": "+str(stime)+"-"+str(etime))
print("Fri") if timetable.meetings['Fri'] else None
for meeting in timetable.meetings['Fri']:
   course_code, class_name, _, stime, etime = meeting
   print("  "+course_code+" "+class_name+": "+str(stime)+"-"+str(etime))

cur.close()
conn.close()

             
