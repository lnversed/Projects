#!/usr/bin/python

import os
import datetime
from datetime import date
import time
import webbrowser as webb

cday = date.today().strftime("%A")
now = datetime.datetime.now()

days = ['Monday','Tuesday','Wednesday','Thursday','Friday']

links = {'geo' : 'https://meet.google.com/oit-kvkq-uus', 'math' : 'https://meet.google.com/evq-stas-gyy', 'french' : 'https://meet.google.com/tpp-srpw-nqj', 'mentor' : 'https://meet.google.com/rrk-ccim-xhw', 'physics' : 'https://meet.google.com/xfq-kjte-ysd', 'eng' : 'https://meet.google.com/fwi-dfgd-ifq', 'german' : 'https://meet.google.com/hjd-dyjy-ypc', 'physical-edu': 'https://meet.google.com/mmp-ukgt-fdt', 'tok' : 'https://meet.google.com/xmd-tekp-tbh'}

program = { 'Monday' : {'physics' : '08:14', 'math' : '09:44', 'physical-edu' : '10:54', 'french' : '13:24'},
            'Tuesday' : {'mentor' : '09:45', 'tok' : '10:54', 'french' : '13:24', 'eng' : '14:09', 'math' : '14:54'},
            'Wednesday' : {'geo' : '08:14', 'french' : '09:46', 'eng' : '10:54', 'german' : '13:24'},
            'Thursday' : {'eng' : '09:45', 'geo' : '10:54', 'math' : '13:24'},
            'Friday' : {'physics' : '16:01', 'german' : '16:05'}}

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

for y in range(len(days)):
	if cday == days[y]:
		today = cday

ordered_class = sorted(program[today].items(), key = lambda x: x[1])
t = program[today].values()
t.sort()

h = [ t[i][:2].lstrip('0') for i in range(len(t)) ]
m = [ t[i][3:].lstrip('0') for i in range(len(t)) ]

times = zip(h,m)

hours = [ times[i][0].lstrip('0') for i in range(len(times)) ]
mins =  [ times[i][1].lstrip('0') for i in range(len(times)) ]

y = lambda b : int(hours[b+1]) - int(hours[b]) 
offsets_h = [ y(i) for i in range(len(hours) - 1) ]
print "Offsets in hours: %s" % offsets_h


x = lambda a : int(mins[a+1]) - int(mins[a]) if a <= 3 else 0
offsets_m = [ x(i) for i in range(len(mins) - 1) ]
print "Offsets in minutes: %s" % offsets_m

print "\n"

sec_h = lambda h: int(offsets_h[h]) * 3600
sh = [ sec_h(i) for i in range(len(offsets_h)) ] 
print "Hours in seconds: %s" %sh

sec_m = lambda m: int(offsets_m[m]) * 60
sm = [ sec_m(i) for i in range(len(offsets_m)) ]
print "Minutes in seconds: %s" %sm

print "\n"

total_sec = [ sh[i] + sm[i] for i in range(len(sm)) ]
print "Total offset in seconds: %s" % total_sec

print "\n"

def Wait():
	noc = len(program[today].keys())
	print "Number of classes today: %s" % noc
	for i in range(noc - 1):
		notify(ordered_class[i][0],"class is starting...")
		webb.get('firefox').open_new_tab(links[ordered_class[i][0]]+"?pli=authuser=1")
		print ordered_class[i][0] + " has started"
		time.sleep(total_sec[i])
	print "School's over!\n"

if now.hour < int(ordered_class[0][1][:2].lstrip('0')):
	class_mins =  ordered_class[0][1][3:].lstrip('0')
	class_hours = ordered_class[0][1][:2]
	offset_m = int(class_mins) - int(now.minute)
	offset_h = int(class_hours) - int(now.hour)
	total_offset = offset_h * 3600 + offset_m * 60
	time.sleep(total_offset)
	Wait()
elif now.hour == int(ordered_class[0][1][:2].lstrip('0')):
	class_min = int(ordered_class[0][1][3:])
	offset = (class_min * 60) - (now.minute*60)
	if offset < 0:
		exit(1)
	time.sleep(offset)
	Wait()

