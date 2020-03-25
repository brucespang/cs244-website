import sys
import yaml
import jinja2
from collections import defaultdict
from datetime import datetime

if len(sys.argv) != 2:
    print("usage: %s path/to/timetable.yaml"%(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

timetable = yaml.safe_load(open(sys.argv[1]).read())

days = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]

errors = 0
def error(str):
    global errors
    print("error: %s"%str, file=sys.stderr)
    errors += 1
    
for day in timetable:
    parsed_date = datetime.strptime(day['date'], "%m/%d/%Y")
    day['parsed_date'] = parsed_date
    day['week'] = parsed_date.isocalendar()[1]
    
    if parsed_date.weekday() not in [1,3]:
        error("{} is a {}, not a Tuesday or a Thursday".format(day['date'], days[parsed_date.weekday()]))

    if day['papers'] is None:
        day['papers'] = []
        
    for paper in day['papers']:
        for field in ['authors','title','url','optional']:
            if field not in paper:
                error("paper for {} missing field '{}'".format(day['date'], field))

    if day['due'] is None:
        day['due'] = []
                
if errors > 0:
    sys.exit(1)

weeks = {}
start_week = timetable[0]['week']
for day in timetable:
    if day['week'] not in weeks:
        weeks[day['week']] = {
            'week': day['week'] - start_week + 1,
            'days': []
        }
        
    weeks[day['week']]['days'].append(day)
    
weeks = sorted(weeks.values(), key=lambda d: d['week'])

template = jinja2.Template(open('src/timetable_table.html.jinja2').read())
print(template.render(weeks=weeks))
