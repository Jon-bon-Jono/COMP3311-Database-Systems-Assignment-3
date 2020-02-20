# Written by Jonathan Williams (z5162987), November 2019
# COMP3311 19T3 Assignment 3

import cs3311
conn = cs3311.connect()

cur = conn.cursor()
#converts weeks string to weeksbinary
def StringToWeeksBinary(string_weeks):
   weeks_binary = ['0']*11
   #handle edge case
   if '<' in string_weeks or 'N' in string_weeks:
      return "".join(weeks_binary)
   #for each week interval specification
   for spec in string_weeks.split(','): 
      if '-' in spec:
         edge_weeks = spec.split('-')
         for w in range(int(edge_weeks[0]), int(edge_weeks[1])+1):
            weeks_binary[w-1]='1'
      else:
         weeks_binary[int(spec)-1]='1'
   return "".join(weeks_binary)


all_meetings_query='''
select m.id, m.weeks
from meetings m
'''
cur.execute(all_meetings_query)
#update all meetings
for tup in cur.fetchall():
   m_id, m_weeks = tup
   update_meeting_query='''
   update meetings
   set weeks_binary = %s
   where id = %s
   '''
   cur.execute(update_meeting_query, [StringToWeeksBinary(m_weeks), m_id])

conn.commit()
cur.close()
conn.close()
