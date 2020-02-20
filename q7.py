# Written by Jonathan Williams (z5162987), November 2019
# COMP3311 19T3 Assignment 3

# This solution ignores double-booking and overlapping class issues

import sys
import cs3311
from datetime import datetime
from datetime import timedelta
conn = cs3311.connect()

cur = conn.cursor()

term = str(sys.argv[1]) if len(sys.argv) >=2 else str("19T1")

#get number of UNSW rooms
num_rooms='''
select count(*) as count
from rooms r
where r.code ilike %s
'''
cur.execute(num_rooms, ["K-%"])
num_rooms_tup = cur.fetchone() 
total_rooms = int(num_rooms_tup[0])

room_use = {} #empty dictionary for room + num hours used in each week

#get data for each meeting
meeting_rooms_query='''
select m.weeks_binary, m.start_time, m.end_time, r.code, r.name, r.id
from meetings m
inner join rooms r on (m.room_id = r.id)
inner join classes cl on (m.class_id = cl.id)
inner join courses co on (cl.course_id = co.id)
inner join terms t on (co.term_id = t.id)
where t.name = %s and r.code ilike %s
'''
cur.execute(meeting_rooms_query, [term, "K-%"])
#for each meeting, add hours for each week to room_use dict
for tup in cur.fetchall():
   weeks, stime, etime, rcode, rname, rid = tup
   #skip these strange cases
   if etime==0 or stime==0:
      continue
   #calculate the length of the meeting
   meeting_length = datetime.strptime(str(etime), '%H%M') - datetime.strptime(str(stime), '%H%M')
   #if dict entry for this room doesn't exist, create one
   if str(rid) not in room_use:
      room_use[str(rid)] = [timedelta()]*10
   #add length of meeting hours to room entry for corresponding weeks
   for i in range(0,10):
      if weeks[i] == '1':
         room_use[str(rid)][i] += meeting_length

underused_room_count = 0
#any room not in the room_use dict, is never used this term and count as underused
underused_room_count += total_rooms - len(room_use.keys())
#count the underused rooms in room_use
for key in room_use.keys():
   avrg = 0
   for time in room_use[key]:
      avrg += time.total_seconds()/3600
   avrg /= 10
   if avrg < 20.0:
      underused_room_count += 1

percentage = (underused_room_count/total_rooms)*100
print(str(round(percentage,1))+"%")

cur.close()
conn.close()
