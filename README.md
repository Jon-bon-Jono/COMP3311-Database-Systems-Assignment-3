# COMP3311-Database-Systems-Assignment-3
8 Exercises written in python/psycopg2 and SQL/PLpgSQL to query the UNSW timetable database

The exercises are as follows:
1. For each course offered in 19T3, produce a list of all courses with a quota more than 50 and that are over-enrolled. I.e. when the number of enrollments exceeds the quota for the course. Results should be ordered by course name (ascending)
1. Someone has asked you "I wonder how many cases there are were 5 UNSW courses share the same 4 numbers in their course code?". Write a solution that produces a list of all different cases where there are X UNSW courses that share the same course code numbers, where X is passed in as the command line argument.
1. Given a 4 letter course code prefix (e.g. COMP) as a command line argument, produce a list of buildings, where for each building a sub-list is produced showing which courses have classes in them during 19T2.
1. Given a 4 letter course code prefix (e.g. COMP) as a command line argument, produce a list of terms (ordered ascending), where for each term a sub-list is produced showing which courses run in that term and how many students are currently enrolled in those courses.
1. For a given course (e.g. COMP1511), find all classes (lectures, tutes, etc) that have less than 50% enrolment in 19T3
1. In the Meetings table, the weeks column currently stores information about the weeks that a meeting runs in the format "1-5,7-10" or "2,4,6,8,10". While this makes sense to a human, it's not a friendly format to use when processing large datasets.
  1. You must write an UPDATE query that takes the text format of the weeks column and outputs a binary format in the column weeks_binary.
  1. For example, "1-5,7-10" would convert to "11111011110", and "2,4,6,8,11" would convert to "01010101001"
  1. If a weeks column contains an 'N' character or a '<' character, this is a strange edge case, and you can convert this to just "00000000000" (all zeroes)
  1. The weeks_binary column is a text string consisting of 11 chars, each of which must be '0' or '1'.
1. What percentage of rooms at UNSW are underused during a term at UNSW? Underused is defined as when across weeks 1-10 inclusive, the room is used on average for less than 20 hours a week
1. Produce a timetable for 19T3 for 1, 2 or 3 courses that aims to minimise the amount of hours being spent in a week on campus or commuting.
